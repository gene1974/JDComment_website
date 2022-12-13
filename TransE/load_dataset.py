
# from

def define_entity():
    entities = [
        'Product',
        'Target',
        'Opinion',
        'Category',
        'Polarity',
    ]
    return entities

def define_relation():
    relations = []
    relations.append(['Product', 'Target', '评价产品'])
    relations.append(['Product', 'Opinion', '产品评价词'])
    relations.append(['Target', 'Opinion', '评价'])
    relations.append(['Category', 'Target', '评价类别'])
    relations.append(['Category', 'Opinion', '类别评价词'])
    relations.append(['Polarity', 'Opinion', '评价极性'])
    return relations

def load_entity(path):
    ent_list = []
    ent_dict = {}
    with open(path, 'r') as f:
        f.readline()
        for line in f:
            ent, ent_id = line.strip().split('\t')
            ent_list.append(ent)
            ent_dict[ent] = int(ent_id)
    assert(len(ent_list) == len(ent_dict))
    return ent_dict

def load_trip(path):
    trip_list = []
    with open(path, 'r') as f:
        f.readline()
        for line in f:
            head, tail, edge = line.strip().split('\t')
            trip_list.append([head, tail, edge])
    return trip_list

def load_entity_label(path):
    ent_label_dict = {}
    ent_label_list = []
    with open(path, 'r') as f:
        # f.readline()
        for line in f:
            ent, ent_label = line.strip().split('\t')
            ent_label_dict[ent] = int(ent_label)
            ent_label_list.append(int(ent_label))
    return ent_label_list


def load_dataset(path = './data/'):
    ent_list = load_entity(path + 'entity2id.txt')
    rel_list = load_entity(path + 'relation2id.txt')
    train_list = load_trip(path + 'train2id.txt')
    valid_list = load_trip(path + 'valid2id.txt')
    test_list = load_trip(path + 'test2id.txt')
    # for bert-cls model
    ent_label_list = load_entity_label(path + 'vocab/entity2label.txt')

    return ent_list, rel_list, train_list, valid_list, test_list, ent_label_list

ent_list, rel_list, train_list, valid_list, test_list, ent_label_list = load_dataset('./data/')
