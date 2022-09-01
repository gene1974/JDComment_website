# -*- coding: utf-8 -*-

import json


def load_json(json_path):
    data_list = []
    with open(json_path, mode="r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line.strip())
            data_list.append(data)
    return data_list


def save_json(data_list, json_path):
    with open(json_path, mode="w", encoding="utf-8") as file:
        for data in data_list:
            file.write(json.dumps(data, ensure_ascii=False) + "\n")
    return None


def cpu_to_gpu(cpu_batch):
    gpu_batch = {}
    for key in cpu_batch.keys():
        gpu_batch[key] = cpu_batch[key].cuda()
    return gpu_batch


def get_span_size(span):
    head, tail = span
    size = tail - head
    return size


def get_span_mask(max_text_len, span):
    head, tail = span
    mask = [0] * max_text_len
    for i in range(head, tail):
        mask[i] = 1
    return mask


def get_context_span(tgt_span, opn_span):
    tgt_head, tgt_tail = tgt_span
    opn_head, opn_tail = opn_span
    if tgt_tail <= opn_head:
        ctx_head = tgt_tail
        ctx_tail = opn_head
    elif opn_tail <= tgt_head:
        ctx_head = opn_tail
        ctx_tail = tgt_head
    else:
        ctx_head = 0
        ctx_tail = 0
    span = (ctx_head, ctx_tail)
    return span


def count_instances(true_list, pred_list):
    true_set = set(true_list)
    pred_set = set(pred_list)
    hits_set = true_set & pred_set
    n_true = len(true_set)
    n_pred = len(pred_set)
    n_hits = len(hits_set)
    return n_true, n_pred, n_hits


def compute_prf(n_true, n_pred, n_hits):
    if n_hits > 0:
        p = n_hits / n_pred
        r = n_hits / n_true
        f = (2 * p * r) / (p + r)
    else:
        p = 0.0
        r = 0.0
        f = 0.0
    return p, r, f
