
from bertmodel import train_bertcls_emb, get_bertcls_emb
from transemodel import get_transe_embeds, train_transe
from visual import visual, visual_compare
# from top import get_top_index, visual_top

from load_dataset import load_dataset, define_entity, define_relation

label_list = define_entity() # ['Product', 'Target', 'Opinion', 'Category', 'Polarity']
label_dict = {label_list[i]: i for i in range(len(label_list))}
rel_type_list = [trip[2] for trip in define_relation()] # ['评价产品', '产品评价词', '评价', '评价类别', '类别评价词', '评价极性']

ent_list, rel_list, train_list, valid_list, test_list, ent_label_list = load_dataset('./data/')

# # train original transe
# print('Train Origin TransE')
# transe, model_time, ent_emb, rel_emb, emb_time = train_transe(ent_list, rel_list, data_path = './data/', mod = 'origin', emb_dim = 768)

# # train bert cls model
# print('Train Bert model')
# model, model_time, bert_emb, rel_emb, emb_time = train_bertcls_emb(ent_list, ent_label_list, len(label_list), rel_type_list)

# train bert initial transe
# print('Train Bert-TransE')
# bert_emb, rel_emb, emb_time = get_bertcls_emb(rel_type_list, len(label_dict), '12121133')
# transe, model_time, ent_emb, rel_emb, emb_time = train_transe(ent_list, rel_list, data_path = './data/', mod = 'bert', emb_time = emb_time, emb_dim = 768)
# ent_emb, rel_emb, emb_time = get_transe_embeds(model_time, ent_list, rel_list, 'origin')

visual(label_list, ent_label_list, '12131104', 'transe')
visual(label_list, ent_label_list, '12121133', 'bert')
visual(label_list, ent_label_list, '12131655', 'bert-transe')

# index = get_top_index(ent_dict, 2000)
# visual_top(label, '10281442', 'transe', index)
# visual_top(label, '10272000', 'bert', index)
# visual_top(label, '10272210', 'bert-transe', index)

# visual_compare(label, '10282032', index)
