# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
from transformers import BertModel
from app.lib.JDComment.code.utils import get_span_mask, get_span_size, get_context_span
from ltp import LTP
nlp = LTP()

class Model(nn.Module):
    def __init__(self, config):
        super(Model, self).__init__()
        # parameters
        self.bert_path = config["bert_path"]  # BERT路径
        self.max_text_len = config["max_text_len"]  # 最大文本长度
        self.max_span_len = config["max_span_len"]  # 最大片段长度
        self.max_num_ents = config["max_num_ents"]  # 最大候选实体数量
        self.max_num_rels = config["max_num_rels"]  # 最大候选关系数量
        self.hidden_size = config["hidden_size"]  # 隐藏状态维度
        self.size_emb_dim = config["size_emb_dim"]  # 宽度嵌入维度
        self.dropout_prob = config["dropout_prob"]  # dropout概率
        self.num_ent_types = 3  # 实体类别数量 (other=0, target=1, opinion=2)
        self.num_rel_types = 2  # 关系类别数量 (none=0, pair=1)
        self.num_categories = config["num_categories"]  # 方面类别数量
        self.num_polarities = config["num_polarities"]  # 极性类别数量
        # modules
        self.encoder = BERTEncoder(bert_path=self.bert_path)
        self.entity_classifier = EntityClassifier(hidden_size=self.hidden_size,
                                                  num_size_emb=self.max_span_len + 1,
                                                  size_emb_dim=self.size_emb_dim,
                                                  dropout_prob=self.dropout_prob,
                                                  num_ent_types=self.num_ent_types,
                                                  num_categories=self.num_categories,
                                                  num_polarities=self.num_polarities)
        self.relation_classifier = RelationClassifier(hidden_size=self.hidden_size,
                                                      num_size_emb=self.max_text_len + 1,
                                                      size_emb_dim=self.size_emb_dim,
                                                      dropout_prob=self.dropout_prob,
                                                      num_rel_types=self.num_rel_types,
                                                      num_categories=self.num_categories,
                                                      num_polarities=self.num_polarities)

    def forward_train(self, token_ids, token_mask, ent_spans, ent_masks, ent_sizes, rel_pairs, rel_masks, rel_sizes):
        # token_ids : (batch_size, max_text_len)
        # token_mask: (batch_size, max_text_len)
        # ent_spans : (batch_size, max_num_ents, 2)
        # ent_masks : (batch_size, max_num_ents, max_text_len)
        # ent_sizes : (batch_size, max_num_ents)
        # rel_pairs  : (batch_size, max_num_rels, 2)
        # rel_masks : (batch_size, max_num_rels, max_text_len)
        # rel_sizes : (batch_size, max_num_rels)
        #
        # ent_type_logits: (batch_size, max_num_ents, num_ent_types)
        # ent_cate_logits: (batch_size, max_num_ents, num_categories)
        # ent_pola_logits: (batch_size, max_num_ents, num_polarities)
        # rel_type_logits: (batch_size, max_num_rels, num_rel_types)
        # rel_cate_logits: (batch_size, max_num_rels, num_categories)
        # rel_pola_logits: (batch_size, max_num_rels, num_polarities)

        hidden_states = self.encoder(token_ids, token_mask)
        ent_type_logits, ent_cate_logits, ent_pola_logits, ent_span_reps, ent_size_embs = self.entity_classifier(hidden_states, ent_spans, ent_masks, ent_sizes)
        rel_type_logits, rel_cate_logits, rel_pola_logits = self.relation_classifier(hidden_states, rel_pairs, rel_masks, rel_sizes, ent_span_reps, ent_size_embs)

        ent_logits = (ent_type_logits, ent_cate_logits, ent_pola_logits)
        rel_logits = (rel_type_logits, rel_cate_logits, rel_pola_logits)
        return ent_logits, rel_logits

    def forward_infer(self, token_ids, token_mask):
        # token_ids : (batch_size, max_text_len)
        # token_mask: (batch_size, max_text_len)
        #
        # ent_spans      : (batch_size, max_num_ents, 2)
        # rel_pairs      : (batch_size, max_num_rels, 2)
        # ent_type_logits: (batch_size, max_num_ents, num_ent_types)
        # ent_cate_logits: (batch_size, max_num_ents, num_categories)
        # ent_pola_logits: (batch_size, max_num_ents, num_polarities)
        # rel_type_logits: (batch_size, max_num_rels, num_rel_types)
        # rel_cate_logits: (batch_size, max_num_rels, num_categories)
        # rel_pola_logits: (batch_size, max_num_rels, num_polarities)

        hidden_states = self.encoder(token_ids, token_mask)
        ent_spans, ent_masks, ent_sizes = self.create_candidate_entities(hidden_states)
        ent_type_logits, ent_cate_logits, ent_pola_logits, ent_span_reps, ent_size_embs = self.entity_classifier(hidden_states, ent_spans, ent_masks, ent_sizes)
        rel_pairs, rel_masks, rel_sizes = self.create_candidate_relations(ent_spans, ent_type_logits)
        rel_type_logits, rel_cate_logits, rel_pola_logits = self.relation_classifier(hidden_states, rel_pairs, rel_masks, rel_sizes, ent_span_reps, ent_size_embs)

        ent_logits = (ent_type_logits, ent_cate_logits, ent_pola_logits)
        rel_logits = (rel_type_logits, rel_cate_logits, rel_pola_logits)
        return ent_spans, rel_pairs, ent_logits, rel_logits

    def create_candidate_entities(self, hidden_states):
        # hidden_states: (batch_size, max_text_len, hidden_size)
        #
        # batch_ent_spans: (batch_size, max_num_ents, 2)
        # batch_ent_masks: (batch_size, max_num_ents, max_text_len)
        # batch_ent_sizes: (batch_size, max_num_ents)

        # candidate entities
        ent_spans = []
        for ent_size in range(1, self.max_span_len + 1):
            for ent_head in range(0, self.max_text_len - ent_size + 1):
                ent_span = (ent_head, ent_head + ent_size)
                ent_spans.append(ent_span)

        ent_masks, ent_sizes = [], []
        for ent_span in ent_spans:
            ent_masks.append(get_span_mask(self.max_text_len, ent_span))
            ent_sizes.append(get_span_size(ent_span))

        # pad entities
        num_ents = len(ent_spans)
        if num_ents < self.max_num_ents:
            ent_span = (0, 0)
            ent_spans += [ent_span] * (self.max_num_ents - num_ents)
            ent_masks += [get_span_mask(self.max_text_len, ent_span)] * (self.max_num_ents - num_ents)
            ent_sizes += [get_span_size(ent_span)] * (self.max_num_ents - num_ents)
        else:
            ent_spans = ent_spans[:self.max_num_ents]
            ent_masks = ent_masks[:self.max_num_ents]
            ent_sizes = ent_sizes[:self.max_num_ents]

        # convert to tensors
        ent_spans = torch.tensor(ent_spans, dtype=torch.long)  # (max_num_ents, 2)
        ent_masks = torch.tensor(ent_masks, dtype=torch.long)  # (max_num_ents, max_text_len)
        ent_sizes = torch.tensor(ent_sizes, dtype=torch.long)  # (max_num_ents)

        # create batch
        batch_size = hidden_states.shape[0]
        batch_ent_spans = ent_spans.unsqueeze(0).repeat(batch_size, 1, 1)  # (batch_size, max_num_ents, 2)
        batch_ent_masks = ent_masks.unsqueeze(0).repeat(batch_size, 1, 1)  # (batch_size, max_num_ents, max_text_len)
        batch_ent_sizes = ent_sizes.unsqueeze(0).repeat(batch_size, 1)  # (batch_size, max_num_ents)
        batch_ent_spans = batch_ent_spans.cuda()
        batch_ent_masks = batch_ent_masks.cuda()
        batch_ent_sizes = batch_ent_sizes.cuda()
        return batch_ent_spans, batch_ent_masks, batch_ent_sizes

    def create_candidate_relations(self, batch_ent_spans, batch_ent_logits):
        # batch_ent_spans : (batch_size, max_num_ents, 2)
        # batch_ent_logits: (batch_size, max_num_ents, num_ent_types)
        #
        # batch_rel_pairs: (batch_size, max_num_rels, 2)
        # batch_rel_masks: (batch_size, max_num_rels, max_text_len)
        # batch_rel_sizes: (batch_size, max_num_rels)

        batch_size = batch_ent_spans.shape[0]
        batch_rel_pairs, batch_rel_masks, batch_rel_sizes = [], [], []
        for i in range(batch_size):
            ent_spans = batch_ent_spans[i]  # (max_num_ents, 2)
            ent_logits = batch_ent_logits[i]  # (max_num_ents, num_ent_types)
            ent_types = torch.argmax(ent_logits, dim=1)  # (max_num_ents)

            # candidate relations
            tgt_indices = torch.nonzero(ent_types == 1).reshape(-1)  # (num_tgt_spans)
            tgt_spans = ent_spans[tgt_indices]  # (num_tgt_spans, 2)
            tgt_indices = tgt_indices.tolist()
            tgt_spans = tgt_spans.tolist()

            opn_indices = torch.nonzero(ent_types == 2).reshape(-1)  # (num_opn_spans)
            opn_spans = ent_spans[opn_indices]  # (num_opn_spans, 2)
            opn_indices = opn_indices.tolist()
            opn_spans = opn_spans.tolist()

            rel_pairs, rel_masks, rel_sizes = [], [], []
            for tgt_idx, tgt_span in zip(tgt_indices, tgt_spans):
                for opn_idx, opn_span in zip(opn_indices, opn_spans):
                    rel_pair = (tgt_idx, opn_idx)
                    rel_span = get_context_span(tgt_span, opn_span)
                    rel_pairs.append(rel_pair)
                    rel_masks.append(get_span_mask(self.max_text_len, rel_span))
                    rel_sizes.append(get_span_size(rel_span))

            # pad relations
            ent_spans = ent_spans.tolist()  # (max_num_ents, 2)
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
            else:
                rel_pairs = rel_pairs[:self.max_num_rels]
                rel_masks = rel_masks[:self.max_num_rels]
                rel_sizes = rel_sizes[:self.max_num_rels]

            # convert to tensors
            rel_pairs = torch.tensor(rel_pairs, dtype=torch.long)  # (max_num_rels, 2)
            rel_masks = torch.tensor(rel_masks, dtype=torch.long)  # (max_num_rels, max_text_len)
            rel_sizes = torch.tensor(rel_sizes, dtype=torch.long)  # (max_num_rels)

            batch_rel_pairs.append(rel_pairs)
            batch_rel_masks.append(rel_masks)
            batch_rel_sizes.append(rel_sizes)

        # create batch
        batch_rel_pairs = torch.stack(batch_rel_pairs)  # (batch_size, max_num_rels, 2)
        batch_rel_masks = torch.stack(batch_rel_masks)  # (batch_size, max_num_rels, max_text_len)
        batch_rel_sizes = torch.stack(batch_rel_sizes)  # (batch_size, max_num_rels)
        batch_rel_pairs = batch_rel_pairs.cuda()
        batch_rel_masks = batch_rel_masks.cuda()
        batch_rel_sizes = batch_rel_sizes.cuda()
        return batch_rel_pairs, batch_rel_masks, batch_rel_sizes


class BERTEncoder(nn.Module):
    def __init__(self, bert_path):
        super(BERTEncoder, self).__init__()
        # parameters
        self.bert_path = bert_path
        # modules
        self.bert = BertModel.from_pretrained(self.bert_path)

    def forward(self, token_ids, token_mask):
        outputs = self.bert(input_ids=token_ids, attention_mask=token_mask, token_type_ids=None)
        hidden_states = outputs.last_hidden_state
        return hidden_states


class EntityClassifier(nn.Module):
    def __init__(self, hidden_size, num_size_emb, size_emb_dim, dropout_prob, num_ent_types, num_categories, num_polarities):
        super(EntityClassifier, self).__init__()
        # parameters
        self.hidden_size = hidden_size
        self.num_size_emb = num_size_emb
        self.size_emb_dim = size_emb_dim
        self.dropout_prob = dropout_prob
        self.num_ent_types = num_ent_types
        self.num_categories = num_categories
        self.num_polarities = num_polarities
        # modules
        self.size_embedding = nn.Embedding(self.num_size_emb, self.size_emb_dim)
        self.dropout = nn.Dropout(self.dropout_prob)
        self.type_classifier = nn.Linear(1 * (self.hidden_size + self.size_emb_dim), self.num_ent_types)
        self.cate_classifier = nn.Linear(1 * (self.hidden_size + self.size_emb_dim), self.num_categories)
        self.pola_classifier = nn.Linear(1 * (self.hidden_size + self.size_emb_dim), self.num_polarities)

    def forward(self, hidden_states, ent_spans, ent_masks, ent_sizes):
        # hidden_states: (batch_size, max_text_len, hidden_size)
        # ent_spans    : (batch_size, max_num_ents, 2)
        # ent_masks    : (batch_size, max_num_ents, max_text_len)
        # ent_sizes    : (batch_size, max_num_ents)
        #
        # ent_type_logits: (batch_size, max_num_ents, num_ent_types)
        # ent_cate_logits: (batch_size, max_num_ents, num_categories)
        # ent_pola_logits: (batch_size, max_num_ents, num_polarities)
        # ent_span_reps  : (batch_size, max_num_ents, hidden_size)
        # ent_size_embs  : (batch_size, max_num_ents, size_emb_dim)

        # entity representations
        batch_size, max_num_ents, _ = ent_spans.shape
        temp_ent_masks = ((ent_masks == 0).float() * (-1e30)).unsqueeze(3)  # (batch_size, max_num_ents, max_text_len, 1)
        temp_hidden_states = hidden_states.unsqueeze(1).repeat(1, max_num_ents, 1, 1)  # (batch_size, max_num_ents, max_text_len, hidden_size)
        ent_span_reps = torch.max(temp_hidden_states + temp_ent_masks, dim=2)[0]  # (batch_size, max_num_ents, hidden_size)

        # entity size embeddings
        ent_size_embs = self.size_embedding(ent_sizes)  # (batch_size, max_num_ents, size_emb_dim)

        # entity classification
        features = torch.cat([ent_span_reps, ent_size_embs], dim=2)  # (batch_size, max_num_ents, 1 * (hidden_size + size_emb_dim))
        features = self.dropout(features)
        ent_type_logits = self.type_classifier(features)  # (batch_size, max_num_ents, num_ent_types)
        ent_cate_logits = self.cate_classifier(features)  # (batch_size, max_num_ents, num_categories)
        ent_pola_logits = self.pola_classifier(features)  # (batch_size, max_num_ents, num_polarities)
        return ent_type_logits, ent_cate_logits, ent_pola_logits, ent_span_reps, ent_size_embs


class RelationClassifier(nn.Module):
    def __init__(self, hidden_size, num_size_emb, size_emb_dim, dropout_prob, num_rel_types, num_categories, num_polarities):
        super(RelationClassifier, self).__init__()
        # parameters
        self.hidden_size = hidden_size
        self.num_size_emb = num_size_emb
        self.size_emb_dim = size_emb_dim
        self.dropout_prob = dropout_prob
        self.num_rel_types = num_rel_types
        self.num_categories = num_categories
        self.num_polarities = num_polarities
        # modules
        self.size_embedding = nn.Embedding(self.num_size_emb, self.size_emb_dim)
        self.dropout = nn.Dropout(self.dropout_prob)
        self.type_classifier = nn.Linear(3 * (self.hidden_size + self.size_emb_dim), self.num_rel_types)
        self.cate_classifier = nn.Linear(3 * (self.hidden_size + self.size_emb_dim), self.num_categories)
        self.pola_classifier = nn.Linear(3 * (self.hidden_size + self.size_emb_dim), self.num_polarities)

    def forward(self, hidden_states, rel_pairs, rel_masks, rel_sizes, ent_span_reps, ent_size_embs):
        # hidden_states: (batch_size, max_text_len, hidden_size)
        # rel_pairs    : (batch_size, max_num_rels, 2)
        # rel_masks    : (batch_size, max_num_rels, max_text_len)
        # rel_sizes    : (batch_size, max_num_rels)
        # ent_span_reps: (batch_size, max_num_ents, hidden_size)
        # ent_size_embs: (batch_size, max_num_ents, size_emb_dim)
        #
        # rel_type_logits: (batch_size, max_num_rels, num_rel_types)
        # rel_cate_logits: (batch_size, max_num_rels, num_categories)
        # rel_pola_logits: (batch_size, max_num_rels, num_polarities)

        # entity pair representations
        batch_size, max_num_rels, _ = rel_pairs.shape
        pair_span_reps = torch.stack([ent_span_reps[i][rel_pairs[i]] for i in range(batch_size)])  # (batch_size, max_num_rels, 2, hidden_size)
        pair_span_reps = pair_span_reps.reshape(batch_size, max_num_rels, -1)  # (batch_size, max_num_rels, 2 * hidden_size)

        # entity pair size embeddings
        pair_size_embs = torch.stack([ent_size_embs[i][rel_pairs[i]] for i in range(batch_size)])  # (batch_size, max_num_rels, 2, size_emb_dim)
        pair_size_embs = pair_size_embs.reshape(batch_size, max_num_rels, -1)  # (batch_size, max_num_rels, 2 * size_emb_dim)

        # context representations
        temp_rel_masks = ((rel_masks == 0).float() * (-1e30)).unsqueeze(3)  # (batch_size, max_num_rels, max_text_len, 1)
        temp_hidden_states = hidden_states.unsqueeze(1).repeat(1, max_num_rels, 1, 1)  # (batch_size, max_num_rels, max_text_len, hidden_size)
        ctx_span_reps = torch.max(temp_hidden_states + temp_rel_masks, dim=2)[0]  # (batch_size, max_num_rels, hidden_size)
        ctx_span_reps[rel_masks.to(torch.uint8).any(-1) == 0] = 0

        # context size embeddings
        ctx_size_embs = self.size_embedding(rel_sizes)  # (batch_size, max_num_rels, size_emb_dim)

        # relation classification
        features = torch.cat([pair_span_reps, pair_size_embs, ctx_span_reps, ctx_size_embs], dim=2)  # (batch_size, max_num_rels, 3 * (hidden_size + size_emb_dim))
        features = self.dropout(features)
        rel_type_logits = self.type_classifier(features)  # (batch_size, max_num_rels, num_rel_types)
        rel_cate_logits = self.cate_classifier(features)  # (batch_size, max_num_rels, num_categories)
        rel_pola_logits = self.pola_classifier(features)  # (batch_size, max_num_rels, num_polarities)
        return rel_type_logits, rel_cate_logits, rel_pola_logits


# debug
if __name__ == "__main__":
    root = "/data1/chenfang/Project/JDComment"

    model_config = {
        "bert_path": "{}/model/bert-base-chinese".format(root),
        "max_text_len": 40,
        "max_span_len": 8,
        "max_num_ents": 320,
        "max_num_rels": 120,
        "hidden_size": 768,
        "size_emb_dim": 20,
        "dropout_prob": 0.1,
        "num_categories": 9,
        "num_polarities": 3,
    }

    model = Model(model_config)
    model.cuda()

    print("---------- model ----------")
    for name, param in model.named_parameters():
        if "bert" not in name:
            print("{}: {}".format(name, list(param.shape)))
    print("---------------------------")
