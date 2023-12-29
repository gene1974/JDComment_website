import os

from visual import translate_cls

def define_relation():
    relation_list = ['价格','品质','色泽','口感','包装','分量','物流','售后', '其他']
    relation_dict = {relation_list[i]: i for i in range(len(relation_list))}
    relation_list_en = translate_cls(relation_list)
    return relation_list, relation_dict

# 数据文件: 五元组
def readDataFile(from_file, max_num = 100000):
    print('Read data_file: {}, set max_num: {}'.format(from_file, max_num))
    relation_list, relation_dict = define_relation()
    entity_dict = {}
    entity_list = []
    trip_list = []
    entity_type_list = [] # 0 for target anf 1 for opinion
    entity_cate_list = [] # category id
    with open(from_file, 'r') as f:
        for line in f.readlines()[:max_num]:
            target, opinion, polarity, product, category = line.strip().split('\t')
            if target not in entity_dict:
                entity_dict[target] = len(entity_dict)
                entity_list.append(target)
                entity_type_list.append(0) # target
                entity_cate_list.append(relation_dict[category]) # category
            if opinion not in entity_dict:
                entity_dict[opinion] = len(entity_dict)
                entity_list.append(opinion)
                entity_type_list.append(1) # opinion
                entity_cate_list.append(relation_dict[category]) # category
            trip_list.append([entity_dict[target], entity_dict[opinion], relation_dict[category]])
    print('Read data_file: {}, entity: {}, trip_list: {}'.format(from_file, len(entity_dict), len(trip_list)))
    return entity_dict, entity_list, trip_list, entity_type_list, entity_cate_list

def addTransEDataFromFile(from_file, to_file):
    os.system('mkdir ' + to_file)
    relation_list, relation_dict = define_relation()
    entity_dict, entity_list, trip_list, entity_type_list, entity_cate_list = readDataFile(from_file)
    dump_graph(entity_list, relation_list, trip_list, path = './data/')
    dump_entity_cls_type(entity_list, entity_type_list, entity_cate_list, to_file)
    return

def dump_entity(path, entities):
    with open(path, 'w') as f:
        f.write(str(len(entities)) + '\n')
        for i in range(len(entities)):
            f.write(entities[i] + '\t' + str(i) + '\n')

def dump_trip(path, triples):
    with open(path, 'w') as f:
        f.write(str(len(triples)) + '\n')
        for i in range(len(triples)):
            f.write(str(triples[i][0]) + '\t' + str(triples[i][1]) + '\t' + str(triples[i][2]) + '\n')

import os
import random
def dump_graph(ent_list, rel_list, trip_list, path = './data/'):
    dump_entity(path + 'entity2id.txt', ent_list)
    dump_entity(path + 'relation2id.txt', rel_list)
    random.shuffle(trip_list)
    print('trip_list:', len(trip_list))
    n_train = int(len(trip_list) * 0.8)
    dump_trip(path + 'train2id.txt', trip_list[:n_train])
    dump_trip(path + 'valid2id.txt', trip_list[n_train:])
    dump_trip(path + 'test2id.txt', trip_list[n_train:])
    os.system('cd data && python n-n.py')

def dump_entity_cls_type(entity_list, entity_type_list, entity_cate_list, to_file):
    relation_list, relation_dict = define_relation()
    relation_list = translate_cls(relation_list)
    ent_type_dict = {0: 'Target', 1: 'Opinion'}
    cls_type_list = ['{}-{}'.format(ent_type, ent_cate) for ent_type in ent_type_dict.values() for ent_cate in relation_list]
    cls_type_dict = {cls_type_list[i]: i for i in range(len(cls_type_list))}
    with open(to_file + 'cls2id.txt', 'w') as f:
        for i in range(len(cls_type_list)):
            f.write('{}\t{}\n'.format(cls_type_list[i], i))
    print('cls_type_list:', cls_type_list)
    
    with open(to_file + 'entity2typeid.txt', 'w') as f:
        for i in range(len(entity_list)):
            ent_type_id = entity_type_list[i]
            ent_cate_id = entity_cate_list[i]
            ent_type = ent_type_dict[ent_type_id]
            ent_cate = relation_list[ent_cate_id]
            cls_type = '{}-{}'.format(ent_type, ent_cate)
            f.write('{}\t{}\t{}-{}\n'.format(i, cls_type_dict[cls_type], ent_type, ent_cate))
    return 

if __name__ == '__main__':
    # add_labeled_triplet_to_graph('./labeled_data.txt')
    addTransEDataFromFile(from_file = '../knowledgebase/unlabel/deduplicate/data.txt', to_file = './data/')
    # define_entity_cls_type()
    
