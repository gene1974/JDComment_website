
from cypher import *

def add_labeled_triplet(file_name = './labeled_data.txt', dump_path = './data/'):
    # graph = ProductGraph()
    # graph.del_all_nodes()
    # graph._init_polar()

    entity = set()
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            item = line.strip().split('\t')
            target, opinion, polarity, product, star, category, date, labeled = item
            # graph.add_data(target, opinion, polarity, product, category)
            entity |= set([target, opinion, polarity, product, category])
            data.append({
                'Product': product,
                'Target': target,
                'Opinion': opinion,
                'Category': category,
                'Polarity': polarity,
            })
    create_graph(data, list(entity), dump_path)
    return data, entity

def define_entity():
    entities = [
        'Product',
        'Opinion',
        'Product',
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

def create_graph(data, ent_list, dump_path):
    # label (neo4j node label)
    label_list = define_entity()
    label_dict = {label_list[i]: i for i in range(len(label_list))}
    
    # relation (egde) type
    relation_type = define_relation()
    rel_list = [item[2] for item in relation_type]
    rel_dict = {rel_list[i]: i for i in range(len(rel_list))}

    # entity (node)
    # ent_list = list(entity)
    ent_dict = {ent_list[i]: i for i in range(len(ent_list))}
    
    trip_list = []
    for item in data:
        for rel in relation_type:
            head, tail, edge = rel # ['Product', 'Target', '评价产品']
            trip_list.append([
                ent_dict[item[head]], 
                ent_dict[item[tail]], 
                rel_dict[edge]
            ])
    dump_graph(ent_list, rel_list, trip_list, dump_path)

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

def dump_graph(ent_list, rel_list, trip_list, path = './data/'):
    dump_entity(path + 'entity2id.txt', ent_list)
    dump_entity(path + 'relation2id.txt', rel_list)
    n_train = int(len(trip_list) * 0.8)
    dump_trip(path + 'train2id.txt', trip_list[:n_train])
    dump_trip(path + 'valid2id.txt', trip_list[n_train:])
    dump_trip(path + 'test2id.txt', trip_list[n_train:])

if __name__ == '__main__':
    add_labeled_triplet('./labeled_data.txt', '../TransE/data/')
