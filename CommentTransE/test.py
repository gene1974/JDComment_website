import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import torch
from torch.autograd import Variable
from OpenKE.openke.config import Trainer, Tester
from OpenKE.openke.module.model import TransE
from OpenKE.openke.data import TestDataLoader, TrainDataLoader

from load_dataset import load_entity
from transemodel import embed_entity

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
    return sorted_idx[:10]

# 将头实体、关系、尾实体的embedding降维画图
def plot_triplet(all_embeds, head_emb, rel_emb, tail_emb, title):
    # data = torch.stack([head_emb, rel_emb, tail_emb], dim = 0)
    data = torch.stack([head_emb, rel_emb], dim = 0)
    data = torch.cat([data, tail_emb], dim = 0)

    # tsne = TSNE(n_components=2, init='pca', random_state=0)
    # data = tsne.fit_transform(data.detach().numpy())
    
    # pca = PCA(n_components=2)
    # pca.fit(all_embeds.detach().numpy())
    # data = pca.transform(data.detach().numpy())
    data = data[:, :2].detach().numpy()

    # 画点和原点之间连接的直线
    plt.figure(figsize = (7.2, 7.2))
    plt.plot([0, data[0, 0]], [0, data[0, 1]], linestyle='--', label = 'head')
    plt.plot([data[0, 0], data[0, 0] + data[1, 0]], [data[0, 1], data[0, 1] + data[1, 1]], linestyle='--', label = 'relation')
    # plt.plot([0, data[i, 0]], [0, data[2, 1]], linestyle='--', label = 'tail')
    for i in range(2, len(data)):
        plt.plot([0, data[i, 0]], [0, data[i, 1]], linestyle='--', label = 'tail', c = 'green')

    plt.legend(['head', 'relation', 'tail'])
    # plt.title(title)
    plt.savefig(f'result/test/{title}.png', dpi = 600)

if __name__ == '__main__':
    print('Test TransE:')
    # load data
    data_path = 'data/'
    model_name = './result/transe_12111305.ckpt'
    # model_name = './result/transe_12101726.ckpt'
    print('load model: ', model_name)

    ent_dict, ent_list = load_entity(data_path + 'entity2id.txt')
    rel_dict, rel_list = load_entity(data_path + 'relation2id.txt')
    
    transe = TransE(
        ent_tot = len(ent_list), # total number of entity
        rel_tot = len(rel_list), # total number of relation
        dim = 768, 
        p_norm = 1, 
        norm_flag = True
    ).cuda()
    transe.load_checkpoint(model_name)

    test_dataloader = TestDataLoader(data_path, "link", True)
    # 获取transe训练得到的所有的embedding
    ent_embeds = embed_entity(transe.ent_embeddings, len(ent_list))
    rel_embeds = embed_entity(transe.rel_embeddings, len(rel_list))
    # 获取测试样本
    with open(data_path + 'test2id.txt', 'r') as f:
        test_triplets = f.readlines()[1:]

    # 测试集上的链接预测结果
    # tester = Tester(model = transe, data_loader = test_dataloader, use_gpu = True)
    # mrr, mr, hit10, hit3, hit1 = tester.run_link_prediction(type_constrain = True)
    # print()

    # 测试集中的前三个样本
    # 打印模型预测的概率最高的前 10 个尾实体
    # print('Tail entity prediction: ')
    # for j in list(range(0, 1000, 50)):
    #     head, tail, relation = map(int, test_triplets[j].strip().split('\t'))
    #     print(ent_list[head], ' + ', rel_list[relation], ' = ', ent_list[tail])
    #     # print(ent_embeds.shape, rel_embeds.shape, )
    #     target = ent_embeds[head] + rel_embeds[relation]
    #     sorted_idx = rank_dist(target.unsqueeze(0), ent_embeds)
    #     for i, index in enumerate(sorted_idx[:10]):
    #         print(i, ': ', ent_list[index])
    #     print()
    
    # # 使用 transe.predict 来预测
    # print('transe.predict: ')
    # for j, [_, data_tail] in enumerate(test_dataloader):
    #     if j == 101:
    #         break
    #     if j not in list(range(0, 1000, 50)): # 取三个测试样本
    #         continue
    #     score = transe.predict({
    #         'batch_h': Variable(torch.from_numpy(data_tail['batch_h']).cuda()),
    #         'batch_t': Variable(torch.from_numpy(data_tail['batch_t']).cuda()),
    #         'batch_r': Variable(torch.from_numpy(data_tail['batch_r']).cuda()),
    #         'mode': data_tail['mode']
    #     }) # score 是距离，距离越小越相似
    #     sorted_idx = sorted(range(len(ent_list)), key = lambda x: score[x])
    #     print('Head: ', ent_list[data_tail['batch_h'].item()], ', Relatioin: ', rel_list[data_tail['batch_r'].item()])
    #     for i, index in enumerate(sorted_idx[:10]):
    #         print(i, ': ', ent_list[index])
    #     print()

    # 选取三个实体
    # 打印和指定实体最相似的前10个实体
    # print('Similar entity prediction: ')
    # # ent_embeds = embed_entity(transe.ent_embeddings, len(ent_list)) # (15817, 200)
    # for target in [ent_dict['花生'], ent_dict['价格'], ent_dict['好吃']] + list(range(10, 20)):
    #     print('Target: ', ent_list[target])
    #     sorted_idx = rank_sim(ent_embeds[target].unsqueeze(0), ent_embeds)
    #     for i, index in enumerate(sorted_idx):
    #         print(i, ': ', ent_list[index])
    #     print()

    # 将头实体、关系、尾实体的embedding降维画图
    # print('Plot triplet: ')
    # head_emb = ent_embeds[ent_dict['花生']]
    # for j in list(range(0, 1000, 50)):

    all_embeds = torch.cat([ent_embeds, rel_embeds])
    pca = PCA(n_components=2)
    pca.fit(all_embeds.detach().numpy())
    ent_embeds = pca.transform(ent_embeds.detach().numpy())
    rel_embeds = pca.transform(rel_embeds.detach().numpy())
    ent_embeds = torch.tensor(ent_embeds)
    rel_embeds = torch.tensor(rel_embeds)

    for j in list(range(1, 10, 2)):
        head, tail, relation = map(int, test_triplets[j].strip().split('\t'))
        target = ent_embeds[head] + rel_embeds[relation]
        sorted_idx = rank_dist(target.unsqueeze(0), ent_embeds)[:10]
        print(ent_list[head], ' + ', rel_list[relation], ' = ', ent_list[sorted_idx[0]])
        title = '{}-{}-{}'.format(ent_list[head], rel_list[relation], ent_list[tail])
        plot_triplet(torch.cat([ent_embeds, rel_embeds]), ent_embeds[head], rel_embeds[relation], ent_embeds[sorted_idx], title = title)
