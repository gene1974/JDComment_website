import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

import argparse

from bertmodel import train_bertcls_emb, get_bertcls_emb
from transemodel import get_transe_embeds, train_transe
from visual import visual, visual_compare
from load_dataset import load_dataset, load_cls_type
from top import visual_top
from create_transe_data import define_relation


# load data
# relation_list, relation_dict = define_relation()
cls_label_dict, cls_label_list = load_cls_type('./data/cls2id.txt')
ent_dict, rel_dict, train_list, valid_list, test_list, ent_label_list = load_dataset('data/')
n_ent = len(ent_dict)
n_rel = len(rel_dict)

def train(mode = 'transe', nbatches = 1000, visual_num = 10000, emb_time = None):
    if mode == 'transe':
        # Train TransE
        print('Train Origin TransE')
        transe, model_time, ent_emb, rel_emb, emb_time = train_transe(
            n_ent, 
            n_rel, 
            mod = 'origin', 
            nbatches = nbatches,
        )
    elif mode == 'bert':
        # Train Bert-cls model
        print('Train Bert classifier')
        model, model_time, bert_emb, rel_emb, emb_time = train_bertcls_emb(
            ent_dict, 
            ent_label_list, 
            n_type          = len(cls_label_list), 
            rel_type_list   = list(rel_dict.keys())
        )
        # Train Bert-init-TransE after Bert-cls
        train('bert-transe', model_time)
    elif mode == 'bert-transe':
        if emb_time is None:
            raise ValueError('emb_time must be given when mode is bert-transe')
        print('Train Bert-TransE')
        transe, model_time, ent_emb, rel_emb, emb_time = train_transe(
            n_ent, 
            n_rel, 
            data_path = './data/', 
            mod = 'bert', 
            emb_time = emb_time, 
            emb_dim = 768
        )
    else:
        raise ValueError('mode must be one of [transe, bert, bert-transe]')
    visual_top(
        all_data_list   = train_list + test_list,
        ent2id_dict     = ent_dict, 
        ent_label_list  = ent_label_list, 
        emb_time    = model_time, 
        mod         = mode, 
        label_list  = cls_label_list, 
        k           = visual_num,
    )

def plot_emb(mode = 'transe', model_time = '12110059', visual_num = 10000):
    # plot embedding
    print('Plot embedding: mode:', mode, ', model_time:', model_time, ', visual_num:', visual_num)
    # ent_emb, rel_emb, emb_time = get_transe_embeds(model_time, n_ent, n_rel, 'origin')
    visual_top(
        all_data_list = train_list + test_list,
        ent2id_dict = ent_dict, 
        ent_label_list = ent_label_list, 
        emb_time = model_time, 
        mod = mode, 
        label_list = cls_label_list, 
        k = visual_num,
    )

# 当前分类最好的模型
# model_time = '12101726'
# ent_emb, rel_emb, emb_time = get_transe_embeds(model_time, n_ent, n_rel, 'origin')
# visual_top(train_list + valid_list + test_list, ent_dict, ent_label_list, model_time, 'transe', cls_label_list, 5000)
# visual_top(train_list + valid_list + test_list, ent_dict, ent_label_list, model_time, 'transe', cls_label_list[9:], 10000)
# visual_top(train_list + valid_list, ent_dict, ent_label_list, model_time, 'transe', cls_label_list, 10000)

# dump embeds
def dump_transe_emb(model_time = '12111305'):
    ent_emb, rel_emb, emb_time = get_transe_embeds(model_time, n_ent, n_rel, 'origin')
    import pickle
    with open('./result/transe_ent_emb.{}.pkl'.format(emb_time), 'wb') as f:
        pickle.dump([ent_dict, ent_emb], f)
    print('Dump TransE embedding: ./result/transe_ent_emb.{}.pkl'.format(emb_time))
    return

# # load_embeds
def load_transe_embeds(model_time):
    import pickle
    ent_dict, ent_emb = pickle.load(open('./result/transe_ent_emb.{}.pkl'.format(model_time), 'rb'))
    ent_emb_dict = {ent: ent_emb[ent_dict[ent]] for ent in ent_dict}
    print('Load TransE embedding: ./result/transe_ent_emb.{}.pkl'.format(model_time))
    return ent_dict, ent_emb

# # Train Bert-cls model
# print('Train Bert classifier')
# model, model_time, bert_emb, rel_emb, emb_time = train_bertcls_emb(ent_dict, ent_label_list, len(cls_label_list), list(rel_dict.keys()))
# load bert embedding
# model_time = '12111045'
# bert_emb, rel_emb, emb_time = get_bertcls_emb(list(rel_dict.keys()), len(cls_label_list), '12111045')
# visual_top(train_list + valid_list, ent_dict, ent_label_list, emb_time, 'bert', cls_label_list, 10000)

# # Train Bert-init-TransE
# print('Train Bert-TransE')
# transe, model_time, ent_emb, rel_emb, emb_time = train_transe(n_ent, n_rel, data_path = './data/', mod = 'bert', emb_time = emb_time, emb_dim = 768)
# visual_top(train_list + valid_list + test_list, ent_dict, ent_label_list, emb_time, 'bert-transe', cls_label_list, 10000)

# model_time = '12111305'
# ent_emb, rel_emb, emb_time = get_transe_embeds(model_time, n_ent, n_rel, 'bert-transe')
# visual_top(train_list + test_list, ent_dict, ent_label_list, model_time, 'bert-transe', cls_label_list, 10000)


# visual_compare(label, '10282032', index)
if __name__ == '__main__':
    train(
        mode = 'transe',
    )
    train(
        mode = 'bert',

    )
