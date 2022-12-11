import json

from data import get_entity
from visual import get_embeds, translate, visual, visual_emb

def cal_num(ent_dict):
    occur = {ent: 0 for ent in ent_dict}
    data = json.load(open('all_output_multi_source_drug_processed.json')) # 171414, 384323
    for line in data['relation']:
        head, tail = line[0], line[1]
        occur[head] += 1
        occur[tail] += 1
    occur = sorted([[ent, occur[ent]] for ent in occur], key = lambda x: x[1], reverse = True)
    return occur

def get_top_index(ent_dict, k = 500):
    occur = cal_num(ent_dict)
    top_occur = occur[:k]
    index = [ent_dict[item[0]] for item in occur[:k]]
    return index

def visual_top(label, emb_time, mod, index):
    legend = ['疾病', '症状','手术', '部位', '药物', '药品名', '生化指标', '实验室检查', '影像学检查', '体格检查', '就诊科室', '其他治疗']
    legend = translate(legend)
    
    if mod == 'transe':
        ent_embeds = get_embeds('./result/transe_emb.vec', emb_time)
        title = 'transe embedding'
    elif mod == 'bert':
        ent_embeds = get_embeds('./result/bert_emb.vec', emb_time)
        title = 'bert embedding'
    elif mod == 'bert-transe':
        ent_embeds = get_embeds('./result/bert_transe_emb.vec', emb_time)
        title = 'bert-transe embedding'
    visual_emb(ent_embeds[index], label[index], title, legend)
    return


if __name__ == '__main__':
    ent_dict, ent_list, ent_name, type_dict, label = get_entity()
    visual_top(ent_dict, ent_list, ent_name, type_dict, label, 2000)