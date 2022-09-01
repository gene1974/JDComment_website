# -*- coding: utf-8 -*-

import argparse


def get_default_args(root):
    parser = argparse.ArgumentParser()

    parser.add_argument("--bert_path", type=str, default="{}/model/bert-base-chinese".format(root))  # BERT
    parser.add_argument("--cate_path", type=str, default="{}/data/category.txt".format(root))  # 方面类别列表
    parser.add_argument("--pola_path", type=str, default="{}/data/polarity.txt".format(root))  # 极性类别列表

    parser.add_argument("--train_data_path", type=str, default="{}/data/train.json".format(root))  # 训练数据
    parser.add_argument("--valid_data_path", type=str, default="{}/data/valid.json".format(root))  # 验证数据
    parser.add_argument("--log_path", type=str, default="{}/model/log.txt".format(root))  # 训练日志
    parser.add_argument("--model_path", type=str, default="{}/model/model.bin".format(root))  # 模型文件

    parser.add_argument("--max_text_len", type=int, default=40)  # 最大文本长度
    parser.add_argument("--max_span_len", type=int, default=8)  # 最大片段长度
    parser.add_argument("--max_num_ents", type=int, default=320)  # 最大候选实体数量 = max_text_len * max_span_len
    parser.add_argument("--max_num_rels", type=int, default=120)  # 最大候选关系数量
    parser.add_argument("--num_neg_ents", type=int, default=100)  # 负采样实体数量
    parser.add_argument("--num_neg_rels", type=int, default=100)  # 负采样关系数量

    parser.add_argument("--hidden_size", type=int, default=768)  # 隐藏状态维度
    parser.add_argument("--size_emb_dim", type=int, default=20)  # 宽度嵌入维度
    parser.add_argument("--dropout_prob", type=float, default=0.1)  # dropout概率
    parser.add_argument("--num_categories", type=int, default=9)  # 方面类别数量
    parser.add_argument("--num_polarities", type=int, default=3)  # 极性类别数量

    parser.add_argument("--bert_lr", type=float, default=2e-5)  # BERT初始学习率
    parser.add_argument("--init_lr", type=float, default=1e-3)  # 其他模块初始学习率
    parser.add_argument("--weight_decay", type=float, default=1e-5)  # 正则项系数
    parser.add_argument("--train_batch_size", type=int, default=32)  # 训练阶段batch大小
    parser.add_argument("--infer_batch_size", type=int, default=32)  # 推理阶段batch大小
    parser.add_argument("--max_num_epochs", type=int, default=50)  # 最大训练epoch
    parser.add_argument("--warm_up_epochs", type=int, default=2)  # 训练热身epoch
    parser.add_argument("--max_no_improve", type=int, default=5)  # 提前结束epoch

    args = parser.parse_args()
    return args
