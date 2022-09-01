# -*- coding: utf-8 -*-

import numpy as np
from tqdm import tqdm
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from transformers import AdamW, get_linear_schedule_with_warmup
from app.lib.JDComment.code.dataset import Dataset
from app.lib.JDComment.code.model import Model
from app.lib.JDComment.code.logger import Logger
from app.lib.JDComment.code.utils import cpu_to_gpu, count_instances, compute_prf



class Factory(object):
    def __init__(self, args):
        self.args = args
        self.dataset = None
        self.model = None

    def print_args(self, logger=None):
        if logger is not None:
            for key in list(vars(self.args).keys()):
                logger.print("{}: {}".format(key, vars(self.args)[key]))
        else:
            for key in list(vars(self.args).keys()):
                print("{}: {}".format(key, vars(self.args)[key]))
        return None

    def print_model(self, model, logger=None):
        if logger is not None:
            for name, param in model.named_parameters():
                if "bert" not in name:
                    logger.print("{}: {}".format(name, list(param.shape)))
        else:
            for name, param in model.named_parameters():
                if "bert" not in name:
                    print("{}: {}".format(name, list(param.shape)))
        return None

    def print_metrics(self, metrics, logger=None):
        if logger is not None:
            logger.print("Tgt(full): {:.4f}, {:.4f}, {:.4f}".format(metrics["tgt_full"][0], metrics["tgt_full"][1], metrics["tgt_full"][2]))
            logger.print("Tgt(span): {:.4f}, {:.4f}, {:.4f}".format(metrics["tgt_span"][0], metrics["tgt_span"][1], metrics["tgt_span"][2]))
            logger.print("Opn(full): {:.4f}, {:.4f}, {:.4f}".format(metrics["opn_full"][0], metrics["opn_full"][1], metrics["opn_full"][2]))
            logger.print("Opn(span): {:.4f}, {:.4f}, {:.4f}".format(metrics["opn_span"][0], metrics["opn_span"][1], metrics["opn_span"][2]))
            logger.print("Rel(full): {:.4f}, {:.4f}, {:.4f}".format(metrics["rel_full"][0], metrics["rel_full"][1], metrics["rel_full"][2]))
            logger.print("Rel(pair): {:.4f}, {:.4f}, {:.4f}".format(metrics["rel_pair"][0], metrics["rel_pair"][1], metrics["rel_pair"][2]))
        else:
            print("Tgt(full): {:.4f}, {:.4f}, {:.4f}".format(metrics["tgt_full"][0], metrics["tgt_full"][1], metrics["tgt_full"][2]))
            print("Tgt(span): {:.4f}, {:.4f}, {:.4f}".format(metrics["tgt_span"][0], metrics["tgt_span"][1], metrics["tgt_span"][2]))
            print("Opn(full): {:.4f}, {:.4f}, {:.4f}".format(metrics["opn_full"][0], metrics["opn_full"][1], metrics["opn_full"][2]))
            print("Opn(span): {:.4f}, {:.4f}, {:.4f}".format(metrics["opn_span"][0], metrics["opn_span"][1], metrics["opn_span"][2]))
            print("Rel(full): {:.4f}, {:.4f}, {:.4f}".format(metrics["rel_full"][0], metrics["rel_full"][1], metrics["rel_full"][2]))
            print("Rel(pair): {:.4f}, {:.4f}, {:.4f}".format(metrics["rel_pair"][0], metrics["rel_pair"][1], metrics["rel_pair"][2]))
        return None

    def get_dataset_config(self):
        dataset_config = {
            "bert_path": self.args.bert_path,
            "cate_path": self.args.cate_path,
            "pola_path": self.args.pola_path,
            "max_text_len": self.args.max_text_len,
            "max_span_len": self.args.max_span_len,
            "max_num_ents": self.args.max_num_ents,
            "max_num_rels": self.args.max_num_rels,
            "num_neg_ents": self.args.num_neg_ents,
            "num_neg_rels": self.args.num_neg_rels,
        }
        return dataset_config

    def get_model_config(self):
        model_config = {
            "bert_path": self.args.bert_path,
            "max_text_len": self.args.max_text_len,
            "max_span_len": self.args.max_span_len,
            "max_num_ents": self.args.max_num_ents,
            "max_num_rels": self.args.max_num_rels,
            "hidden_size": self.args.hidden_size,
            "size_emb_dim": self.args.size_emb_dim,
            "dropout_prob": self.args.dropout_prob,
            "num_categories": self.args.num_categories,
            "num_polarities": self.args.num_polarities,
        }
        return model_config

    def save_model(self, model, model_path):
        params = model.state_dict()
        with open(model_path, "wb") as file:
            torch.save(params, file)
        return None

    def load_model(self, model, model_path):
        with open(model_path, "rb") as file:
            params = torch.load(file)
        model.load_state_dict(params)
        return model

    def train_one_epoch(self, dataset, dataloader, model, loss_function, optimizer, scheduler):
        bar = tqdm(total=dataset.num_instances)
        model.train()
        for batch in dataloader:
            batch = cpu_to_gpu(batch)
            optimizer.zero_grad()
            ent_logits, rel_logits = model.forward_train(token_ids=batch["token_ids"],
                                                         token_mask=batch["token_mask"],
                                                         ent_spans=batch["ent_spans"],
                                                         ent_masks=batch["ent_masks"],
                                                         ent_sizes=batch["ent_sizes"],
                                                         rel_pairs=batch["rel_pairs"],
                                                         rel_masks=batch["rel_masks"],
                                                         rel_sizes=batch["rel_sizes"])
            ent_type_logits, ent_cate_logits, ent_pola_logits = ent_logits
            rel_type_logits, rel_cate_logits, rel_pola_logits = rel_logits

            ent_type_loss = loss_function(ent_type_logits.reshape(-1, model.num_ent_types), batch["ent_types"].reshape(-1))
            ent_cate_loss = loss_function(ent_cate_logits.reshape(-1, model.num_categories), batch["ent_cates"].reshape(-1))
            ent_pola_loss = loss_function(ent_pola_logits.reshape(-1, model.num_polarities), batch["ent_polas"].reshape(-1))
            rel_type_loss = loss_function(rel_type_logits.reshape(-1, model.num_rel_types), batch["rel_types"].reshape(-1))
            rel_cate_loss = loss_function(rel_cate_logits.reshape(-1, model.num_categories), batch["rel_cates"].reshape(-1))
            rel_pola_loss = loss_function(rel_pola_logits.reshape(-1, model.num_polarities), batch["rel_polas"].reshape(-1))
            loss = (ent_type_loss + ent_cate_loss + ent_pola_loss) + (rel_type_loss + rel_cate_loss + rel_pola_loss)
            loss.backward()
            optimizer.step()
            scheduler.step()

            batch_size = batch["token_ids"].shape[0]
            bar.set_description("loss={:.4f}".format(loss.item()))
            bar.update(batch_size)
        bar.close()
        return None

    def predict(self, dataset, dataloader, model):
        all_ent_spans = np.zeros([dataset.num_instances, dataset.max_num_ents, 2], dtype=np.int64)
        all_rel_pairs = np.zeros([dataset.num_instances, dataset.max_num_rels, 2], dtype=np.int64)
        all_ent_types = np.zeros([dataset.num_instances, dataset.max_num_ents], dtype=np.int64)
        all_ent_cates = np.zeros([dataset.num_instances, dataset.max_num_ents], dtype=np.int64)
        all_ent_polas = np.zeros([dataset.num_instances, dataset.max_num_ents], dtype=np.int64)
        all_rel_types = np.zeros([dataset.num_instances, dataset.max_num_rels], dtype=np.int64)
        all_rel_cates = np.zeros([dataset.num_instances, dataset.max_num_rels], dtype=np.int64)
        all_rel_polas = np.zeros([dataset.num_instances, dataset.max_num_rels], dtype=np.int64)

        offset = 0
        model.eval()
        for batch in dataloader:
            batch = cpu_to_gpu(batch)
            with torch.no_grad():
                ent_spans, rel_pairs, ent_logits, rel_logits = model.forward_infer(token_ids=batch["token_ids"],
                                                                                   token_mask=batch["token_mask"])
            ent_type_logits, ent_cate_logits, ent_pola_logits = ent_logits
            rel_type_logits, rel_cate_logits, rel_pola_logits = rel_logits

            ent_spans = ent_spans.detach().cpu().numpy()  # (batch_size, max_num_ents, 2)
            rel_pairs = rel_pairs.detach().cpu().numpy()  # (batch_size, max_num_rels, 2)
            ent_type_logits = ent_type_logits.detach().cpu().numpy()  # (batch_size, max_num_ents, num_ent_types)
            ent_cate_logits = ent_cate_logits.detach().cpu().numpy()  # (batch_size, max_num_ents, num_categories)
            ent_pola_logits = ent_pola_logits.detach().cpu().numpy()  # (batch_size, max_num_ents, num_polarities)
            rel_type_logits = rel_type_logits.detach().cpu().numpy()  # (batch_size, max_num_rels, num_rel_types)
            rel_cate_logits = rel_cate_logits.detach().cpu().numpy()  # (batch_size, max_num_rels, num_categories)
            rel_pola_logits = rel_pola_logits.detach().cpu().numpy()  # (batch_size, max_num_rels, num_polarities)

            ent_types = np.argmax(ent_type_logits, axis=2)  # (batch_size, max_num_ents)
            ent_cates = np.argmax(ent_cate_logits, axis=2)  # (batch_size, max_num_ents)
            ent_polas = np.argmax(ent_pola_logits, axis=2)  # (batch_size, max_num_ents)
            rel_types = np.argmax(rel_type_logits, axis=2)  # (batch_size, max_num_rels)
            rel_cates = np.argmax(rel_cate_logits, axis=2)  # (batch_size, max_num_rels)
            rel_polas = np.argmax(rel_pola_logits, axis=2)  # (batch_size, max_num_rels)

            batch_size = batch["token_ids"].shape[0]
            all_ent_spans[offset:offset + batch_size] = ent_spans
            all_rel_pairs[offset:offset + batch_size] = rel_pairs
            all_ent_types[offset:offset + batch_size] = ent_types
            all_ent_cates[offset:offset + batch_size] = ent_cates
            all_ent_polas[offset:offset + batch_size] = ent_polas
            all_rel_types[offset:offset + batch_size] = rel_types
            all_rel_cates[offset:offset + batch_size] = rel_cates
            all_rel_polas[offset:offset + batch_size] = rel_polas
            offset += batch_size

        outputs = {
            "ent_spans": all_ent_spans,
            "rel_pairs": all_rel_pairs,
            "ent_types": all_ent_types,
            "ent_cates": all_ent_cates,
            "ent_polas": all_ent_polas,
            "rel_types": all_rel_types,
            "rel_cates": all_rel_cates,
            "rel_polas": all_rel_polas,
        }
        return outputs

    def decode(self, dataset, outputs):
        results = []
        for idx in range(dataset.num_instances):
            ent_spans = outputs["ent_spans"][idx]  # (max_num_ents, 2)
            rel_pairs = outputs["rel_pairs"][idx]  # (max_num_rels, 2)
            ent_types = outputs["ent_types"][idx]  # (max_num_ents) (other=0, target=1, opinion=2)
            ent_cates = outputs["ent_cates"][idx]  # (max_num_ents)
            ent_polas = outputs["ent_polas"][idx]  # (max_num_ents)
            rel_types = outputs["rel_types"][idx]  # (max_num_rels) (none=0, pair=1)
            rel_cates = outputs["rel_cates"][idx]  # (max_num_rels)
            rel_polas = outputs["rel_polas"][idx]  # (max_num_rels)

            tgt_labels = []  # 对象: [(tgt_head, tgt_tail, category, polarity)]
            opn_labels = []  # 观点: [(opn_head, opn_tail, category, polarity)]
            rel_labels = []  # 关系: [(tgt_head, tgt_tail, opn_head, opn_tail, category, polarity)]

            # decode targets and opinions
            for i in range(dataset.max_num_ents):
                ent_head = ent_spans[i][0]
                ent_tail = ent_spans[i][1]
                category = dataset.idx2cate[ent_cates[i]]
                polarity = dataset.idx2pola[ent_polas[i]]
                if (ent_head == 0) or (ent_tail == 0):
                    continue  # 跳过填充实体
                if ent_types[i] == 1:  # target: ent_type=1
                    tgt_labels.append((ent_head, ent_tail, category, polarity))  # 此处为分词后的字符索引
                if ent_types[i] == 2:  # opinion: ent_type=2
                    opn_labels.append((ent_head, ent_tail, category, polarity))  # 此处为分词后的字符索引

            # decode relations
            for i in range(dataset.max_num_rels):
                tgt_idx = rel_pairs[i][0]
                opn_idx = rel_pairs[i][1]
                tgt_head = ent_spans[tgt_idx][0]
                tgt_tail = ent_spans[tgt_idx][1]
                opn_head = ent_spans[opn_idx][0]
                opn_tail = ent_spans[opn_idx][1]
                category = dataset.idx2cate[rel_cates[i]]
                polarity = dataset.idx2pola[rel_polas[i]]
                if (tgt_head == 0) or (tgt_tail == 0) or (opn_head == 0) or (opn_tail == 0):
                    continue  # 跳过填充关系
                if rel_types[i] == 1:  # pair: rel_type=1
                    rel_labels.append((tgt_head, tgt_tail, opn_head, opn_tail, category, polarity))  # 此处为分词后的字符索引

            # decode comment_units
            units = []
            tgt_set = set()
            opn_set = set()
            for tgt_head, tgt_tail, opn_head, opn_tail, category, polarity in rel_labels:
                tgt_span = (tgt_head, tgt_tail)
                opn_span = (opn_head, opn_tail)
                tgt_set.add(tgt_span)
                opn_set.add(opn_span)
                unit = (tgt_head - 1, tgt_tail - 1, opn_head - 1, opn_tail - 1, category, polarity)  # 此处为原始字符索引
                units.append(unit)
            for tgt_head, tgt_tail, category, polarity in tgt_labels:
                tgt_span = (tgt_head, tgt_tail)
                if tgt_span in tgt_set:
                    continue
                tgt_set.add(tgt_span)
                unit = (tgt_head - 1, tgt_tail - 1, None, None, category, polarity)  # 此处为原始字符索引
                units.append(unit)
            for opn_head, opn_tail, category, polarity in opn_labels:
                opn_span = (opn_head, opn_tail)
                if opn_span in opn_set:
                    continue
                opn_set.add(opn_span)
                unit = (None, None, opn_head - 1, opn_tail - 1, category, polarity)  # 此处为原始字符索引
                units.append(unit)

            result = {
                "tgt_labels": tgt_labels,
                "opn_labels": opn_labels,
                "rel_labels": rel_labels,
                "comment_units": units,
            }
            results.append(result)
        return results

    def evaluate(self, dataset, results):
        n_true_tgt_full, n_pred_tgt_full, n_hits_tgt_full = 0, 0, 0
        n_true_tgt_span, n_pred_tgt_span, n_hits_tgt_span = 0, 0, 0
        n_true_opn_full, n_pred_opn_full, n_hits_opn_full = 0, 0, 0
        n_true_opn_span, n_pred_opn_span, n_hits_opn_span = 0, 0, 0
        n_true_rel_full, n_pred_rel_full, n_hits_rel_full = 0, 0, 0
        n_true_rel_pair, n_pred_rel_pair, n_hits_rel_pair = 0, 0, 0

        for idx in range(dataset.num_instances):
            true_tgt_fulls = dataset.instances[idx].tgt_labels
            pred_tgt_fulls = results[idx]["tgt_labels"]
            n_true, n_pred, n_hits = count_instances(true_tgt_fulls, pred_tgt_fulls)
            n_true_tgt_full += n_true
            n_pred_tgt_full += n_pred
            n_hits_tgt_full += n_hits

            true_tgt_spans = [(tgt_head, tgt_tail) for tgt_head, tgt_tail, tgt_cate, tgt_pola in true_tgt_fulls]
            pred_tgt_spans = [(tgt_head, tgt_tail) for tgt_head, tgt_tail, tgt_cate, tgt_pola in pred_tgt_fulls]
            n_true, n_pred, n_hits = count_instances(true_tgt_spans, pred_tgt_spans)
            n_true_tgt_span += n_true
            n_pred_tgt_span += n_pred
            n_hits_tgt_span += n_hits

            true_opn_fulls = dataset.instances[idx].opn_labels
            pred_opn_fulls = results[idx]["opn_labels"]
            n_true, n_pred, n_hits = count_instances(true_opn_fulls, pred_opn_fulls)
            n_true_opn_full += n_true
            n_pred_opn_full += n_pred
            n_hits_opn_full += n_hits

            true_opn_spans = [(opn_head, opn_tail) for opn_head, opn_tail, opn_cate, opn_pola in true_opn_fulls]
            pred_opn_spans = [(opn_head, opn_tail) for opn_head, opn_tail, opn_cate, opn_pola in pred_opn_fulls]
            n_true, n_pred, n_hits = count_instances(true_opn_spans, pred_opn_spans)
            n_true_opn_span += n_true
            n_pred_opn_span += n_pred
            n_hits_opn_span += n_hits

            true_rel_fulls = dataset.instances[idx].rel_labels
            pred_rel_fulls = results[idx]["rel_labels"]
            n_true, n_pred, n_hits = count_instances(true_rel_fulls, pred_rel_fulls)
            n_true_rel_full += n_true
            n_pred_rel_full += n_pred
            n_hits_rel_full += n_hits

            true_rel_pairs = [(tgt_head, tgt_tail, opn_head, opn_tail) for tgt_head, tgt_tail, opn_head, opn_tail, rel_cate, rel_pola in true_rel_fulls]
            pred_rel_pairs = [(tgt_head, tgt_tail, opn_head, opn_tail) for tgt_head, tgt_tail, opn_head, opn_tail, rel_cate, rel_pola in pred_rel_fulls]
            n_true, n_pred, n_hits = count_instances(true_rel_pairs, pred_rel_pairs)
            n_true_rel_pair += n_true
            n_pred_rel_pair += n_pred
            n_hits_rel_pair += n_hits

        tgt_full_p, tgt_full_r, tgt_full_f = compute_prf(n_true_tgt_full, n_pred_tgt_full, n_hits_tgt_full)
        tgt_span_p, tgt_span_r, tgt_span_f = compute_prf(n_true_tgt_span, n_pred_tgt_span, n_hits_tgt_span)
        opn_full_p, opn_full_r, opn_full_f = compute_prf(n_true_opn_full, n_pred_opn_full, n_hits_opn_full)
        opn_span_p, opn_span_r, opn_span_f = compute_prf(n_true_opn_span, n_pred_opn_span, n_hits_opn_span)
        rel_full_p, rel_full_r, rel_full_f = compute_prf(n_true_rel_full, n_pred_rel_full, n_hits_rel_full)
        rel_pair_p, rel_pair_r, rel_pair_f = compute_prf(n_true_rel_pair, n_pred_rel_pair, n_hits_rel_pair)
        metrics = {
            "tgt_full": (tgt_full_p, tgt_full_r, tgt_full_f),
            "tgt_span": (tgt_span_p, tgt_span_r, tgt_span_f),
            "opn_full": (opn_full_p, opn_full_r, opn_full_f),
            "opn_span": (opn_span_p, opn_span_r, opn_span_f),
            "rel_full": (rel_full_p, rel_full_r, rel_full_f),
            "rel_pair": (rel_pair_p, rel_pair_r, rel_pair_f),
        }
        return metrics

    def train(self):
        # logger
        logger = Logger(self.args.log_path)

        logger.print("---------- args ----------")
        self.print_args(logger)
        logger.print("--------------------------")

        # dataset config
        dataset_config = self.get_dataset_config()

        # training dataset
        train_dataset = Dataset(dataset_config, train_mode=True)
        logger.print("building training dataset from {}".format(self.args.train_data_path))
        train_dataset.load_data_from_file(self.args.train_data_path)
        train_sampler = RandomSampler(train_dataset)
        train_dataloader = DataLoader(train_dataset, sampler=train_sampler, batch_size=self.args.train_batch_size)
        logger.print("number of training instances: {}".format(len(train_dataset)))

        # validation dataset
        valid_dataset = Dataset(dataset_config, train_mode=False)
        logger.print("building validation dataset from {}".format(self.args.valid_data_path))
        valid_dataset.load_data_from_file(self.args.valid_data_path)
        valid_sampler = SequentialSampler(valid_dataset)
        valid_dataloader = DataLoader(valid_dataset, sampler=valid_sampler, batch_size=self.args.train_batch_size)
        logger.print("number of validation instances: {}".format(len(valid_dataset)))

        # model config
        model_config = self.get_model_config()

        # model
        model = Model(model_config)
        model.cuda()

        logger.print("---------- model ----------")
        self.print_model(model, logger)
        logger.print("---------------------------")

        # loss function
        loss_function = nn.CrossEntropyLoss(ignore_index=-1)

        # optimizer
        no_decay = ["bias", "LayerNorm.weight", "LayerNorm.bias"]
        optimizer_grouped_parameters = [
            {"params": [p for n, p in model.named_parameters() if ("bert" in n) and not any(nd in n for nd in no_decay)],
             "lr": self.args.bert_lr,
             "weight_decay": self.args.weight_decay,
             },
            {"params": [p for n, p in model.named_parameters() if ("bert" in n) and any(nd in n for nd in no_decay)],
             "lr": self.args.bert_lr,
             "weight_decay": 0.0,
             },
            {"params": [p for n, p in model.named_parameters() if ("bert" not in n) and not any(nd in n for nd in no_decay)],
             "lr": self.args.init_lr,
             "weight_decay": self.args.weight_decay,
             },
            {"params": [p for n, p in model.named_parameters() if ("bert" not in n) and any(nd in n for nd in no_decay)],
             "lr": self.args.init_lr,
             "weight_decay": 0.0,
             },
        ]
        optimizer = AdamW(optimizer_grouped_parameters, eps=1e-8)

        # scheduler
        max_num_steps = len(train_dataloader) * self.args.max_num_epochs
        warm_up_steps = len(train_dataloader) * self.args.warm_up_epochs
        scheduler = get_linear_schedule_with_warmup(optimizer,
                                                    num_warmup_steps=warm_up_steps,
                                                    num_training_steps=max_num_steps)

        # train
        num_no_improve = 0
        best_epoch = 0
        best_score = 0.0
        best_metrics = {}
        for epoch in range(self.args.max_num_epochs):
            logger.print("----------------------------------------")
            logger.print("epoch: {}/{}".format(epoch + 1, self.args.max_num_epochs))
            # 训练
            self.train_one_epoch(dataset=train_dataset,
                                 dataloader=train_dataloader,
                                 model=model,
                                 loss_function=loss_function,
                                 optimizer=optimizer,
                                 scheduler=scheduler)
            # 预测
            valid_outputs = self.predict(dataset=valid_dataset,
                                         dataloader=valid_dataloader,
                                         model=model)
            # 解码
            valid_results = self.decode(dataset=valid_dataset,
                                        outputs=valid_outputs)
            # 评估
            valid_metrics = self.evaluate(dataset=valid_dataset,
                                          results=valid_results)

            # print metrics
            valid_score = (valid_metrics["tgt_full"][2] + valid_metrics["opn_full"][2] + valid_metrics["rel_full"][2]) / 3.0
            logger.print("validation score: {:.4f}".format(valid_score))
            self.print_metrics(valid_metrics, logger)

            # early stop
            if valid_score >= best_score:
                num_no_improve = 0
                best_epoch = epoch + 1
                best_score = valid_score
                best_metrics = valid_metrics
                logger.print("saving model to {}".format(self.args.model_path))
                self.save_model(model, self.args.model_path)
            else:
                num_no_improve += 1
                if num_no_improve == self.args.max_no_improve:
                    break

        # print best metrics
        logger.print("----------------------------------------")
        logger.print("best epoch: {}".format(best_epoch))
        logger.print("best score: {:.4f}".format(best_score))
        self.print_metrics(best_metrics, logger)
        return None

    def initialize(self):
        print("---------- args ----------")
        self.print_args()
        print("--------------------------")

        # dataset
        dataset_config = self.get_dataset_config()
        self.dataset = Dataset(dataset_config, train_mode=False)

        # model
        model_config = self.get_model_config()
        self.model = Model(model_config)
        print("loading model from {}".format(self.args.model_path))
        self.model = self.load_model(self.model, self.args.model_path)
        self.model.cuda()
        return None

    def infer(self, data_list):
        # 载入数据
        self.dataset.load_data_from_list(data_list)
        sampler = SequentialSampler(self.dataset)
        dataloader = DataLoader(self.dataset, sampler=sampler, batch_size=self.args.infer_batch_size)

        # 预测：评论 >> 实体与关系类别
        outputs = self.predict(dataset=self.dataset,
                               dataloader=dataloader,
                               model=self.model)
        # 解码：实体与关系类别 >> 评价对象，观点表达，评价搭配
        results = self.decode(dataset=self.dataset,
                              outputs=outputs)
        return results
