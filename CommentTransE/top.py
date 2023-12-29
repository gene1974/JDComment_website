import json
import numpy as np

from visual import get_embeds, translate, visual, visual_emb

def get_top_index(all_data_list, ent2id_dict, k = 500):
    entid_occur = {ent2id_dict[ent]: 0 for ent in ent2id_dict}
    for line in all_data_list:
        head_id, tail_id = int(line[0]), int(line[1])
        entid_occur[head_id] += 1
        entid_occur[tail_id] += 1
    entid_occur = sorted([[entid, entid_occur[entid]] for entid in entid_occur], key = lambda x: x[1], reverse = True)
    top_ent_ids = [item[0] for item in entid_occur[:k]]
    return top_ent_ids

def visual_top(all_data_list, ent2id_dict, ent_label_list, emb_time, mod, label_list, k = 500):
    top_ent_ids = get_top_index(all_data_list, ent2id_dict, k)
    
    if mod == 'transe':
        ent_embeds = get_embeds('./result/transe_emb.vec', emb_time)
        title = 'TransE'
    elif mod == 'bert':
        ent_embeds = get_embeds('./result/bert_emb.vec', emb_time)
        title = 'Bert'
    elif mod == 'bert-transe':
        ent_embeds = get_embeds('./result/bert_transe_emb.vec', emb_time)
        title = 'Bert-TransE'
    else:
        raise ValueError('mod must be transe, bert or bert-transe')
    ent_label_list = np.array(ent_label_list)
    visual_emb(ent_embeds[top_ent_ids], ent_label_list[top_ent_ids], title + '_' + emb_time, label_list)
    return


if __name__ == '__main__':
    from load_dataset import load_dataset, get_defined_type
    label_list, label_dict, rel_type_list = get_defined_type()
    ent2id_dict, rel2id_dict, train_list, valid_list, test_list, ent_label_list = load_dataset('data/')
    visual_top(test_list, ent2id_dict, ent_label_list, '12071630', 'transe', label_list, 200)
