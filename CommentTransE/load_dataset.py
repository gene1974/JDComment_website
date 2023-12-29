import os

def load_entity(path):
    ent_list = []
    ent2id_dict = {}
    with open(path, 'r') as f:
        f.readline()
        for line in f:
            ent, ent_id = line.strip().split('\t')
            ent_list.append(ent)
            ent2id_dict[ent] = int(ent_id)
    assert(len(ent_list) == len(ent2id_dict))
    return ent2id_dict, ent_list

def load_trip(path):
    trip_list = []
    with open(path, 'r') as f:
        f.readline()
        for line in f:
            head, tail, edge = line.strip().split('\t')
            trip_list.append([head, tail, edge])
    return trip_list

def load_entity_label(path = './data/entity2typeid.txt'):
    ent_label_dict = {}
    ent_label_list = []
    with open(path, 'r') as f:
        for line in f:
            ent, ent_label = line.strip().split('\t')[:2]
            ent_label_dict[ent] = int(ent_label)
            ent_label_list.append(int(ent_label))
    return ent_label_list

def load_cls_type(path = './data/cls2id.txt'):
    cls2id_dict = {}
    cls_label_list = []
    with open(path, 'r') as f:
        for line in f:
            cls, cls_id = line.strip().split('\t')
            cls2id_dict[cls] = int(cls_id)
            cls_label_list.append(cls)
    return cls2id_dict, cls_label_list

def load_dataset(path = './data/'):
    ent2id_dict, ent_list = load_entity(path + 'entity2id.txt')
    rel2id_dict, rel_list = load_entity(path + 'relation2id.txt')
    train_list = load_trip(path + 'train2id.txt')
    valid_list = load_trip(path + 'valid2id.txt')
    test_list = load_trip(path + 'test2id.txt')
    # for bert-cls model
    ent_label_list = load_entity_label(path + 'entity2typeid.txt')
    return ent2id_dict, rel2id_dict, train_list, valid_list, test_list, ent_label_list

if __name__ == '__main__':
    ent2id_dict, rel2id_dict, train_list, valid_list, test_list, ent_label_list = load_dataset('./data/')
