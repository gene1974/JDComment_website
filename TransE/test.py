import numpy as np
import torch
from torch.autograd import Variable
from OpenKE.openke.config import Trainer, Tester
from OpenKE.openke.module.model import TransE
from OpenKE.openke.data import TestDataLoader, TrainDataLoader

from data import load_entity
from utils import get_embeds

def rank_sim(target, ent_embeds):
    n_ent = ent_embeds.shape[0]
    ent_sims = torch.zeros((n_ent, ))
    batch_size = 16
    begin = 0
    while begin < n_ent:
        end = min(n_ent, begin + batch_size)
        ent_sims[begin: end] = torch.cosine_similarity(target, ent_embeds[begin: end], dim = -1)
        begin += batch_size
    sorted_idx = sorted(range(n_ent), key = lambda x: ent_sims[x], reverse = True)
    return sorted_idx[1:11]

def rank_dist(target, ent_embeds):
    n_ent = ent_embeds.shape[0]
    ent_sims = torch.zeros((n_ent, ))
    batch_size = 16
    begin = 0
    while begin < n_ent:
        end = min(n_ent, begin + batch_size)
        ent_sims[begin: end] = torch.cdist(target, ent_embeds[begin: end], p = 2)
        begin += batch_size
    sorted_idx = sorted(range(n_ent), key = lambda x: ent_sims[x])
    return sorted_idx[1:11]

if __name__ == '__main__':
    # load data
    data_path = 'drugdata/'
    model_name = './checkpoint/transe_drug_10231123.ckpt'
    print('load model: ', model_name)

    ent_dict, ent_list = load_entity(data_path + 'entity2id.txt')
    rel_dict, rel_list = load_entity(data_path + 'relation2id.txt')
    
    transe = TransE(
        ent_tot = 81607, # total number of entity
        rel_tot = 15,
        dim = 768, 
        p_norm = 1, 
        norm_flag = True
    ).cuda()
    transe.load_checkpoint(model_name)

    # 测试集上的链接预测结果
    test_dataloader = TestDataLoader("./drugdata/", "link", True)
    tester = Tester(model = transe, data_loader = test_dataloader, use_gpu = True)
    mrr, mr, hit10, hit3, hit1 = tester.run_link_prediction(type_constrain = True)
    print()

    # 测试集中的前三个样本
    # 打印模型预测的概率最高的前 10 个尾实体
    print('Tail entity prediction: ')
    # 获取transe训练得到的所有的embedding
    ent_embeds = get_embeds(transe.ent_embeddings, ent_list)
    rel_embeds = get_embeds(transe.rel_embeddings, rel_list)
    # 获取测试样本
    with open('drugdata/test2id.txt', 'r') as f:
        test_triplets = f.readlines()
    for j in [30, 50, 70]:
        head, tail, relation = map(int, test_triplets[j].strip().split('\t'))
        print(ent_list[head], ' + ', rel_list[relation], ' = ', ent_list[tail])
        # print(ent_embeds.shape, rel_embeds.shape, )
        target = ent_embeds[head] + rel_embeds[relation]
        sorted_idx = rank_dist(target.unsqueeze(0), ent_embeds)
        for i, index in enumerate(sorted_idx[:10]):
            print(i, ': ', ent_list[index])
        print()
    
    # 使用 transe.predict 来预测
    print('Similar entity prediction(predict): ')
    for j, [_, data_tail] in enumerate(test_dataloader):
        if j == 101:
            break
        if j not in [0, 50, 100]: # 取三个测试样本
            continue
        score = transe.predict({
            'batch_h': Variable(torch.from_numpy(data_tail['batch_h']).cuda()),
            'batch_t': Variable(torch.from_numpy(data_tail['batch_t']).cuda()),
            'batch_r': Variable(torch.from_numpy(data_tail['batch_r']).cuda()),
            'mode': data_tail['mode']
        }) # score 是距离，距离越小越相似
        sorted_idx = sorted(range(len(ent_list)), key = lambda x: score[x])
        print('Head: ', ent_list[data_tail['batch_h'].item()], ', Relatioin: ', rel_list[data_tail['batch_r'].item()])
        for i, index in enumerate(sorted_idx[:10]):
            print(i, ': ', ent_list[index])
        print()

    # 选取三个实体
    # 打印和指定实体最相似的前10个实体
    print('Similar entity prediction: ')
    # ent_embeds = get_embeds(transe.ent_embeddings, ent_list) # (15817, 200)
    for target in [ent_dict['四维他胶囊'], ent_dict['心房壁'], ent_dict['镫骨足弓间']]:
        print('Target: ', ent_list[target])
        sorted_idx = rank_sim(ent_embeds[target].unsqueeze(0), ent_embeds)
        for i, index in enumerate(sorted_idx):
            print(i, ': ', ent_list[index])
        print()
        
