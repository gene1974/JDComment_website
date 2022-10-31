
from cypher import *

def add_labeled_triplet():
    knowledge_base = []
    with open('./labeled_data.txt', 'r') as f:
        for line in f:
            data = line.strip().split('\t')
            knowledge_base.append(data)

    graph = ProductGraph()
    graph.del_all_nodes()

    for item in knowledge_base:
        entity, opinion, polarity, product, star, category, date, labeled = item
        graph.add_data(entity, opinion, polarity, product, category)

if __name__ == '__main__':
    add_labeled_triplet()
