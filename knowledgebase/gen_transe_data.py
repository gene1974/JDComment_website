
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

def dump_entity_label(path, ent_list, ent_label_dict):
    with open(path, 'w') as f:
        # f.write(str(len(ent_list)) + '\n')
        for i in range(len(ent_list)):
            f.write(str(ent_list[i]) + '\t' + str(ent_label_dict[ent_list[i]]) + '\n')

def dump_graph(ent_list, rel_list, trip_list, ent_label_dict, path = './data/'):
    dump_entity(path + 'entity2id.txt', ent_list)
    dump_entity(path + 'relation2id.txt', rel_list)
    n_train = int(len(trip_list) * 0.8)
    dump_trip(path + 'train2id.txt', trip_list[:n_train])
    dump_trip(path + 'valid2id.txt', trip_list[n_train:])
    dump_trip(path + 'test2id.txt', trip_list[n_train:])
    # for bert-cls model
    dump_entity_label(path + 'vocab/entity2label.txt', ent_list, ent_label_dict)

def get_labeled_data(file_name = './labeled_data.txt'):
    polar_dict = {'POS': '正面', 'NEU': '中性', 'NEG': '负面'}
    ent_list = []
    ent_dict = {}
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            item = line.strip().split('\t')
            target, opinion, polarity, product, star, category, date, labeled = item
            for ent in [target, opinion, polar_dict[polarity], product, category]:
                if ent not in ent_dict:
                    ent_dict[ent] = len(ent_dict)
                    ent_list.append(ent)
            data.append({
                'Product': product,
                'Target': target,
                'Opinion': opinion,
                'Category': category,
                'Polarity': polar_dict[polarity],
            })
    return data, ent_list

def create_graph(file_name = './labeled_data.txt', dump_path = './data/'):
    data, ent_list = get_labeled_data(file_name)
    # label (neo4j node label)
    label_list = define_entity()
    label_dict = {label_list[i]: i for i in range(len(label_list))}
    
    # relation (egde) type
    relation_type = define_relation()
    rel_list = [item[2] for item in relation_type]
    rel_dict = {rel_list[i]: i for i in range(len(rel_list))}

    # entity (node)
    ent_dict = {ent_list[i]: i for i in range(len(ent_list))}
    ent_label_dict = {}
    
    trip_list = []
    for item in data:
        for label in item:
            ent_label_dict[item[label]] = label_dict[label]
        for rel in relation_type:
            head, tail, edge = rel # ['Product', 'Target', '评价产品']
            trip_list.append([
                ent_dict[item[head]], 
                ent_dict[item[tail]], 
                rel_dict[edge]
            ])
    dump_graph(ent_list, rel_list, trip_list, ent_label_dict, dump_path)

if __name__ == '__main__':
    create_graph('./labeled_data.txt', './data/')
    create_graph('./labeled_data.txt', '../TransE/data/')
