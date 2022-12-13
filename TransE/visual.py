import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import torch
from OpenKE.openke.module.model import TransE
from transformers import BertTokenizer, BertModel
from sklearn.manifold import TSNE

from bertmodel import get_bertcls_emb
from transemodel import get_transe_embeds
from utils import load_data, save_data

def translate(legend):
    ent_translate_dict = {
        '疾病':     'Disease',
        '症状':     'Symptom',
        '手术':     'Surgery',
        '部位':     'Anatomy',
        '药物':     'Drug',
        '药品名':   'Drug Name',
        '生化指标': 'Biochemical Indicator',
        '实验室检查':   'Lab Exam',
        '影像学检查':   'Radiographic Exam',
        '体格检查': 'Physical Exam',
        '就诊科室': 'Medical Department',
        '其他治疗': 'Other treatment',
    }
    rel_translate_dict = {
        '症状': 'Disease-Symptom',
        '部位': 'Disease-Anatomy',
        '检查': 'Disease-Exam',
        '科室': 'Disease-Department',
        '指标': 'Disease-Indicator',
        '疾病相关指标': 'Exam-Indicator',
        '并发症': 'Complication',
        '规范化药品名称': 'Name Normalization',
        '治疗': 'Treatment',
        '抗炎': 'Anti-inflammatory',
        '抗病毒': 'Anti-viral',
        '止痛': 'Pain Relief',
        '解热': 'Antipyretic',
    }
    legend = [ent_translate_dict[ent] for ent in legend]
    return legend

# plot
def plot_embedding(data, label, title, legend):
    label = np.array(label)
    print(label)
    print(data)
    print(legend)
    x_min, x_max = np.min(data, 0), np.max(data, 0)
    data = (data - x_min) / (x_max - x_min)
    fig = plt.figure(figsize = (7.2, 7.2))

    for i in range(len(legend) - 1, -1, -1):
        print(i, len(data[label == i, 0]))
        plt.plot(data[label == i, 0], data[label == i, 1], '.')
    plt.title(title)
    plt.legend(legend)
    model_time = time.strftime('%m%d%H%M', time.localtime())
    plt.savefig('./fig/' + title + '.' + model_time + '.png', dpi = 600)
    fig.legend(loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
    return fig

# plot
def plot_compare_embedding(data, label, title, legend, index):
    x_min, x_max = np.min(data, 0), np.max(data, 0)
    data = (data - x_min) / (x_max - x_min)
    fig = plt.figure(figsize = (23, 7))
    # plt.axis('equal')
    # color_list = plt.cm.tab20([0, 2, 3, 6, 5, 18, 8, 10, 12, 14, 16, 5])
    # color_list = plt.cm.rainbow(np.linspace(0, 1, 13))
    sns.set()
    color_list = sns.color_palette("Paired", 12)
    # color_list = sns.color_palette("hls", 12)

    # origin
    plt.subplot(1, 3, 1)
    # plt.axis('equal')
    # plt.gca().set_aspect('equal', adjustable='box')
    for i in range(len(legend) - 1, -1, -1):
        plt.plot(data[label == i, 0], data[label == i, 1], '.', markersize = '5', c = color_list[i])
    # plt.gca().set_aspect('equal', adjustable='box')
    plt.title(title)

    # top 1000
    data = data[index]
    label = label[index]
    ax2 = plt.subplot(1, 3, 2)
    # plt.gca().set_aspect('equal', adjustable='box')
    for i in range(len(legend) - 1, -1, -1):
        plt.plot(data[label == i, 0], data[label == i, 1], '.', markersize = '10', c = color_list[i], label = legend[i])
    plt.title(title + '(Top ' + str(len(index)) + ')')
    handles,labels = ax2.get_legend_handles_labels()
    handles.reverse()
    labels.reverse()
    plt.legend(handles, labels, bbox_to_anchor=(1.05, 0), loc = 3, borderaxespad = 0)
    # plt.gca().set_aspect('equal', adjustable='box')

    model_time = time.strftime('%m%d%H%M', time.localtime())
    plt.savefig('./fig/' + title + '.' + model_time + '.pdf', dpi = 300, bbox_inches='tight')
    # with open()
    return fig

def get_embeds(path, data_time = None):
    ent_embeds, rel_embeds = load_data(path, data_time)
    return ent_embeds

def dim_reduction(ent_embeds):
    tsne = TSNE(n_components=2, init='pca', random_state=0)
    result = tsne.fit_transform(ent_embeds.detach().numpy())
    print('tsne:', result.shape)
    return result

def visual_emb(ent_embeds, label, title, legend):
    result = dim_reduction(ent_embeds)
    plot_embedding(result, label, title, legend)

def visual(legend, label, emb_time, mod = 'transe'):
    if mod == 'transe':
        ent_embeds = get_embeds('./result/transe_emb.vec', emb_time)
        title = 'transe embedding'
    elif mod == 'bert':
        ent_embeds = get_embeds('./result/bert_emb.vec', emb_time)
        title = 'bert embedding'
    elif mod == 'bert-transe':
        ent_embeds = get_embeds('./result/bert_transe_emb.vec', emb_time)
        title = 'bert-transe embedding'
    visual_emb(ent_embeds, label, title, legend)
    return ent_embeds, label, title, legend

def visual_compare(label, emb_time, index):
    legend = ['疾病', '症状','手术', '部位', '药物', '药品名', '生化指标', '实验室检查', '影像学检查', '体格检查', '就诊科室', '其他治疗']
    legend = translate(legend)
    # ent_embeds = get_embeds('./result/bert_transe_emb.vec', emb_time)
    # ent_embeds = dim_reduction(ent_embeds)
    # save_data('./result/reduced_bert_transe_emb.vec', ent_embeds)
    ent_embeds = load_data('./result/reduced_bert_transe_emb.vec', emb_time)
    title = 'Graph Embedding'
    
    plot_compare_embedding(ent_embeds, label, title, legend, index)
    return

if __name__ == '__main__':
    ent_dict, ent_list, ent_name, ent_type, type_dict, label, \
        rel_dict, rel_list, triplets = load_vocab()
    # print(type_dict, rel_dict)
    visual(ent_list, ent_name, type_dict, label, 'bertcls')
    # visual('transe', '10222237')


