# -*- coding: utf-8 -*-

import random
import torch
from torch.utils.data import Dataset as TorchDataset
from transformers import BertTokenizer
from app.lib.JDComment.code.utils import load_json, get_span_mask, get_span_size, get_context_span
from ltp import LTP
nlp = LTP()

class Instance(object):
    def __init__(self):
        self.text = None  # 评论
        self.token_ids = None
        self.token_mask = None

        self.units = None  # 标签（原始字符索引）: [(tgt_head, tgt_tail, opn_head, opn_tail, category, polarity)]
        self.tgt_labels = None  # 对象（分词后字符索引）: [(tgt_head, tgt_tail, category, polarity)]
        self.opn_labels = None  # 观点（分词后字符索引）: [(opn_head, opn_tail, category, polarity)]
        self.rel_labels = None  # 关系（分词后字符索引）: [(tgt_head, tgt_tail, opn_head, opn_tail, category, polarity)]


class Dataset(TorchDataset):
    def __init__(self, config, train_mode):
        self.bert_path = config["bert_path"]  # BERT路径
        self.cate_path = config["cate_path"]  # 方面类别列表
        self.pola_path = config["pola_path"]  # 极性类别列表
        self.max_text_len = config["max_text_len"]  # 最大文本长度
        self.max_span_len = config["max_span_len"]  # 最大片段长度
        self.max_num_ents = config["max_num_ents"]  # 最大候选实体数量
        self.max_num_rels = config["max_num_rels"]  # 最大候选关系数量
        self.num_neg_ents = config["num_neg_ents"]  # 负采样实体数量
        self.num_neg_rels = config["num_neg_rels"]  # 负采样关系数量
        self.train_mode = train_mode  # 是否训练模式

        self.tokenizer = BertTokenizer.from_pretrained(self.bert_path)

        # 方面的类别索引
        self.category_list = []
        with open(self.cate_path, mode="r", encoding="utf-8") as file:
            for line in file:
                category = line.strip()
                self.category_list.append(category)
        self.num_categories = len(self.category_list)
        self.cate2idx = {}
        self.idx2cate = {}
        for idx, cate in enumerate(self.category_list):
            self.cate2idx[cate] = idx
            self.idx2cate[idx] = cate

        # 极性的类别索引
        self.polarity_list = []
        with open(self.pola_path, mode="r", encoding="utf-8") as file:
            for line in file:
                polarity = line.strip()
                self.polarity_list.append(polarity)
        self.num_polarities = len(self.polarity_list)
        self.pola2idx = {}
        self.idx2pola = {}
        for idx, pola in enumerate(self.polarity_list):
            self.pola2idx[pola] = idx
            self.idx2pola[idx] = pola

        self.data_list = []  # 原始数据列表
        self.instances = []  # 处理后的数据列表
        self.num_instances = 0

    def __len__(self):
        return self.num_instances

    def __getitem__(self, idx):
        if self.train_mode:
            return self.create_train_item(idx)
        else:
            return self.create_infer_item(idx)

    def load_data_from_file(self, data_path):
        self.data_list = load_json(data_path)
        self.set_instances()
        return None

    def load_data_from_list(self, data_list):
        self.data_list = data_list
        self.set_instances()
        return None

    def set_instances(self):
        self.instances = []
        for data in self.data_list:
            # create instance
            instance = Instance()
            # process text
            instance.text = data["comment_text"]
            outputs = self.tokenizer(text=instance.text,
                                     padding="max_length",
                                     truncation="only_first",
                                     max_length=self.max_text_len,
                                     return_attention_mask=True)
            instance.token_ids = outputs["input_ids"]
            instance.token_mask = outputs["attention_mask"]
            # process annotations
            if "comment_units" in data:
                instance.units = []
                for unit in data["comment_units"]:
                    if unit["target"] is not None:
                        tgt_head = unit["target"]["head"]
                        tgt_tail = unit["target"]["tail"]
                    else:
                        tgt_head = None
                        tgt_tail = None
                    if unit["opinion"] is not None:
                        opn_head = unit["opinion"]["head"]
                        opn_tail = unit["opinion"]["tail"]
                    else:
                        opn_head = None
                        opn_tail = None
                    category = unit["aspect"]
                    polarity = unit["polarity"]
                    instance.units.append((tgt_head, tgt_tail, opn_head, opn_tail, category, polarity))  # 此处为原始字符索引
                tgt_set = set()
                opn_set = set()
                rel_set = set()
                for tgt_head, tgt_tail, opn_head, opn_tail, category, polarity in instance.units:
                    if (tgt_head is not None) and (tgt_tail is not None) and (tgt_head + 1 < self.max_text_len) and (tgt_tail + 1 < self.max_text_len):
                        tgt_set.add((tgt_head + 1, tgt_tail + 1, category, polarity))
                    if (opn_head is not None) and (opn_tail is not None) and (opn_head + 1 < self.max_text_len) and (opn_tail + 1 < self.max_text_len):
                        opn_set.add((opn_head + 1, opn_tail + 1, category, polarity))
                    if (tgt_head is not None) and (tgt_tail is not None) and (opn_head is not None) and (opn_tail is not None) and (tgt_head + 1 < self.max_text_len) and (
                            tgt_tail + 1 < self.max_text_len) and (opn_head + 1 < self.max_text_len) and (opn_tail + 1 < self.max_text_len):
                        rel_set.add((tgt_head + 1, tgt_tail + 1, opn_head + 1, opn_tail + 1, category, polarity))
                instance.tgt_labels = sorted(list(tgt_set), reverse=False)  # 此处为分词后的字符索引
                instance.opn_labels = sorted(list(opn_set), reverse=False)  # 此处为分词后的字符索引
                instance.rel_labels = sorted(list(rel_set), reverse=False)  # 此处为分词后的字符索引
            # save instance
            self.instances.append(instance)
        self.num_instances = len(self.instances)
        return None

    def create_train_item(self, idx):
        instance = self.instances[idx]

        # positive entities (entity type: other=0, target=1, opinion=2)
        pos_ent_spans, pos_ent_masks, pos_ent_sizes, pos_ent_types, pos_ent_cates, pos_ent_polas = [], [], [], [], [], []
        for ent_head, ent_tail, category, polarity in instance.tgt_labels:
            ent_span = (ent_head, ent_tail)
            if (ent_span in pos_ent_spans) or (get_span_size(ent_span) > self.max_span_len):
                continue  # 实体已存在 或 实体长度超过限制
            pos_ent_spans.append(ent_span)
            pos_ent_masks.append(get_span_mask(self.max_text_len, ent_span))
            pos_ent_sizes.append(get_span_size(ent_span))
            pos_ent_types.append(1)  # target: ent_type=1
            pos_ent_cates.append(self.cate2idx[category])
            pos_ent_polas.append(self.pola2idx[polarity])
        for ent_head, ent_tail, category, polarity in instance.opn_labels:
            ent_span = (ent_head, ent_tail)
            if (ent_span in pos_ent_spans) or (get_span_size(ent_span) > self.max_span_len):
                continue  # 实体已存在 或 实体长度超过限制
            pos_ent_spans.append(ent_span)
            pos_ent_masks.append(get_span_mask(self.max_text_len, ent_span))
            pos_ent_sizes.append(get_span_size(ent_span))
            pos_ent_types.append(2)  # opinion: ent_type=2
            pos_ent_cates.append(self.cate2idx[category])
            pos_ent_polas.append(self.pola2idx[polarity])

        # negative entities (entity type: other=0, target=1, opinion=2)
        neg_ent_spans = []
        for ent_size in range(1, self.max_span_len + 1):
            for ent_head in range(0, self.max_text_len - ent_size + 1):
                ent_span = (ent_head, ent_head + ent_size)
                if ent_span in pos_ent_spans:
                    continue  # 实体为正例
                neg_ent_spans.append(ent_span)
        neg_ent_spans = random.sample(neg_ent_spans, min(len(neg_ent_spans), self.num_neg_ents))

        neg_ent_masks, neg_ent_sizes, neg_ent_types, neg_ent_cates, neg_ent_polas = [], [], [], [], []
        for ent_span in neg_ent_spans:
            neg_ent_masks.append(get_span_mask(self.max_text_len, ent_span))
            neg_ent_sizes.append(get_span_size(ent_span))
            neg_ent_types.append(0)  # other: ent_type=0
            neg_ent_cates.append(-1)
            neg_ent_polas.append(-1)

        # merge entities
        ent_spans = pos_ent_spans + neg_ent_spans
        ent_masks = pos_ent_masks + neg_ent_masks
        ent_sizes = pos_ent_sizes + neg_ent_sizes
        ent_types = pos_ent_types + neg_ent_types
        ent_cates = pos_ent_cates + neg_ent_cates
        ent_polas = pos_ent_polas + neg_ent_polas

        # positive relations (relation type: none=0, pair=1)
        pos_rel_pairs, pos_rel_masks, pos_rel_sizes, pos_rel_types, pos_rel_cates, pos_rel_polas = [], [], [], [], [], []
        for tgt_head, tgt_tail, opn_head, opn_tail, category, polarity in instance.rel_labels:
            tgt_span = (tgt_head, tgt_tail)
            opn_span = (opn_head, opn_tail)
            rel_span = get_context_span(tgt_span, opn_span)
            if (get_span_size(tgt_span) > self.max_span_len) or (get_span_size(opn_span) > self.max_span_len):
                continue  # 实体长度超过限制
            tgt_idx = ent_spans.index(tgt_span)
            opn_idx = ent_spans.index(opn_span)
            rel_pair = (tgt_idx, opn_idx)
            if rel_pair in pos_rel_pairs:
                continue  # 实体对已存在
            pos_rel_pairs.append(rel_pair)
            pos_rel_masks.append(get_span_mask(self.max_text_len, rel_span))
            pos_rel_sizes.append(get_span_size(rel_span))
            pos_rel_types.append(1)  # pair: rel_type=1
            pos_rel_cates.append(self.cate2idx[category])
            pos_rel_polas.append(self.pola2idx[polarity])

        # negative relations (relation type: none=0, pair=1)
        com_neg_rel_pairs = []
        for tgt_span in pos_ent_spans:
            for opn_span in pos_ent_spans:
                tgt_idx = ent_spans.index(tgt_span)
                opn_idx = ent_spans.index(opn_span)
                rel_pair = (tgt_idx, opn_idx)
                if (tgt_idx == opn_idx) or (rel_pair in pos_rel_pairs):
                    continue  # 头尾实体相同 或 实体对为正例
                com_neg_rel_pairs.append(rel_pair)

        opt_neg_rel_pairs = []
        for tgt_span in pos_ent_spans:
            for opn_span in neg_ent_spans:
                tgt_idx = ent_spans.index(tgt_span)
                opn_idx = ent_spans.index(opn_span)
                rel_pair = (tgt_idx, opn_idx)
                opt_neg_rel_pairs.append(rel_pair)
        for tgt_span in neg_ent_spans:
            for opn_span in pos_ent_spans:
                tgt_idx = ent_spans.index(tgt_span)
                opn_idx = ent_spans.index(opn_span)
                rel_pair = (tgt_idx, opn_idx)
                opt_neg_rel_pairs.append(rel_pair)

        if len(com_neg_rel_pairs) < self.num_neg_rels:
            opt_neg_rel_pairs = random.sample(opt_neg_rel_pairs, min(len(opt_neg_rel_pairs), self.num_neg_rels - len(com_neg_rel_pairs)))
            neg_rel_pairs = com_neg_rel_pairs + opt_neg_rel_pairs
        else:
            neg_rel_pairs = random.sample(com_neg_rel_pairs, min(len(com_neg_rel_pairs), self.num_neg_rels))

        neg_rel_masks, neg_rel_sizes, neg_rel_types, neg_rel_cates, neg_rel_polas = [], [], [], [], []
        for tgt_idx, opn_idx in neg_rel_pairs:
            tgt_span = ent_spans[tgt_idx]
            opn_span = ent_spans[opn_idx]
            rel_span = get_context_span(tgt_span, opn_span)
            neg_rel_masks.append(get_span_mask(self.max_text_len, rel_span))
            neg_rel_sizes.append(get_span_size(rel_span))
            neg_rel_types.append(0)  # none: rel_type=0
            neg_rel_cates.append(-1)
            neg_rel_polas.append(-1)

        # merge relations
        rel_pairs = pos_rel_pairs + neg_rel_pairs
        rel_masks = pos_rel_masks + neg_rel_masks
        rel_sizes = pos_rel_sizes + neg_rel_sizes
        rel_types = pos_rel_types + neg_rel_types
        rel_cates = pos_rel_cates + neg_rel_cates
        rel_polas = pos_rel_polas + neg_rel_polas

        # pad entities
        num_ents = len(ent_spans)
        if num_ents < self.max_num_ents:
            ent_span = (0, 0)
            ent_spans += [ent_span] * (self.max_num_ents - num_ents)
            ent_masks += [get_span_mask(self.max_text_len, ent_span)] * (self.max_num_ents - num_ents)
            ent_sizes += [get_span_size(ent_span)] * (self.max_num_ents - num_ents)
            ent_types += [-1] * (self.max_num_ents - num_ents)
            ent_cates += [-1] * (self.max_num_ents - num_ents)
            ent_polas += [-1] * (self.max_num_ents - num_ents)
        else:
            ent_spans = ent_spans[:self.max_num_ents]
            ent_masks = ent_masks[:self.max_num_ents]
            ent_sizes = ent_sizes[:self.max_num_ents]
            ent_types = ent_types[:self.max_num_ents]
            ent_cates = ent_cates[:self.max_num_ents]
            ent_polas = ent_polas[:self.max_num_ents]

        # pad relations
        num_rels = len(rel_pairs)
        if num_rels < self.max_num_rels:
            tgt_idx = self.max_num_ents - 1
            opn_idx = self.max_num_ents - 1
            rel_pair = (tgt_idx, opn_idx)
            tgt_span = ent_spans[tgt_idx]
            opn_span = ent_spans[opn_idx]
            rel_span = get_context_span(tgt_span, opn_span)
            rel_pairs += [rel_pair] * (self.max_num_rels - num_rels)
            rel_masks += [get_span_mask(self.max_text_len, rel_span)] * (self.max_num_rels - num_rels)
            rel_sizes += [get_span_size(rel_span)] * (self.max_num_rels - num_rels)
            rel_types += [-1] * (self.max_num_rels - num_rels)
            rel_cates += [-1] * (self.max_num_rels - num_rels)
            rel_polas += [-1] * (self.max_num_rels - num_rels)
        else:
            rel_pairs = rel_pairs[:self.max_num_rels]
            rel_masks = rel_masks[:self.max_num_rels]
            rel_sizes = rel_sizes[:self.max_num_rels]
            rel_types = rel_types[:self.max_num_rels]
            rel_cates = rel_cates[:self.max_num_rels]
            rel_polas = rel_polas[:self.max_num_rels]

        item = {
            "token_ids": torch.tensor(instance.token_ids, dtype=torch.long),
            "token_mask": torch.tensor(instance.token_mask, dtype=torch.long),
            "ent_spans": torch.tensor(ent_spans, dtype=torch.long),
            "ent_masks": torch.tensor(ent_masks, dtype=torch.long),
            "ent_sizes": torch.tensor(ent_sizes, dtype=torch.long),
            "ent_types": torch.tensor(ent_types, dtype=torch.long),
            "ent_cates": torch.tensor(ent_cates, dtype=torch.long),
            "ent_polas": torch.tensor(ent_polas, dtype=torch.long),
            "rel_pairs": torch.tensor(rel_pairs, dtype=torch.long),
            "rel_masks": torch.tensor(rel_masks, dtype=torch.long),
            "rel_sizes": torch.tensor(rel_sizes, dtype=torch.long),
            "rel_types": torch.tensor(rel_types, dtype=torch.long),
            "rel_cates": torch.tensor(rel_cates, dtype=torch.long),
            "rel_polas": torch.tensor(rel_polas, dtype=torch.long),
        }
        return item

    def create_infer_item(self, idx):
        instance = self.instances[idx]
        item = {
            "token_ids": torch.tensor(instance.token_ids, dtype=torch.long),
            "token_mask": torch.tensor(instance.token_mask, dtype=torch.long),
        }
        return item


# debug
if __name__ == "__main__":
    from torch.utils.data import DataLoader, SequentialSampler

    root = "/data1/chenfang/Project/JDComment"
    dataset_config = {
        "bert_path": "{}/model/bert-base-chinese".format(root),
        "cate_path": "{}/data/category.txt".format(root),
        "pola_path": "{}/data/polarity.txt".format(root),
        "max_text_len": 40,
        "max_span_len": 8,
        "max_num_ents": 320,
        "max_num_rels": 120,
        "num_neg_ents": 100,
        "num_neg_rels": 100,
    }
    data_path = "{}/data/valid.json".format(root)
    batch_size = 8

    dataset = Dataset(dataset_config, train_mode=True)
    print("building dataset from {}".format(data_path))
    dataset.load_data_from_file(data_path)
    sampler = SequentialSampler(dataset)
    dataloader = DataLoader(dataset, sampler=sampler, batch_size=batch_size)
    print("number of training instances: {}".format(len(dataset)))

    ins_idx = 14
    item = dataset[ins_idx]

    print(dataset.tokenizer.convert_ids_to_tokens(item["token_ids"]))

    print("ent_spans:", item["ent_spans"].shape)
    print(item["ent_spans"][0:5])
    print("ent_masks:", item["ent_masks"].shape)
    print(item["ent_masks"][0:5])
    print("ent_sizes:", item["ent_sizes"].shape)
    print(item["ent_sizes"][0:5])
    print("ent_types:", item["ent_types"].shape)
    print(item["ent_types"][0:5])
    print("ent_cates:", item["ent_cates"].shape)
    print(item["ent_cates"][0:5])
    print("ent_polas:", item["ent_polas"].shape)
    print(item["ent_polas"][0:5])

    print("rel_pairs:", item["rel_pairs"].shape)
    print(item["rel_pairs"][0:5])
    print("rel_masks:", item["rel_masks"].shape)
    print(item["rel_masks"][0:5])
    print("rel_sizes:", item["rel_sizes"].shape)
    print(item["rel_sizes"][0:5])
    print("rel_types:", item["rel_types"].shape)
    print(item["rel_types"][0:5])
    print("rel_cates:", item["rel_cates"].shape)
    print(item["rel_cates"][0:5])
    print("rel_polas:", item["rel_polas"].shape)
    print(item["rel_polas"][0:5])
