import sys
from py2neo import Graph, Node, Relationship
from py2neo import NodeMatcher,RelationshipMatcher

# 模糊匹配：https://www.cnblogs.com/edkong/p/16167542.html
# 用label表示图谱类型：Product

class Neo4jGraph(object):
    def __init__(self, host = 'http://localhost:7474', auth = ('neo4j', 'neo4j')):
        self.host = host
        self.auth = auth
        self.graph = Graph(host, auth = auth)
        self.node_matcher = NodeMatcher(self.graph)
        self.rel_matcher = RelationshipMatcher(self.graph)

    # 添加一个节点，更新节点属性；不会重复添加；
    def add_node(self, label, properties = {}):
        if 'name' not in properties:
            sys.stderr.write('Property `name` is required, get:', properties, '\n')
            return None
        node = self.find_one_node(label, {'name': properties['name']})
        if node is None:
            node  = Node(label, **properties)
            self.graph.create(node)
        for prop in properties:
            if prop != 'name':
                node[prop] = properties[prop]
                self.graph.push(node)
        return node

    def get_node(self, label, properties = {}):
        return self.add_node(label, properties)

    # 返回图谱中匹配label和properties的所有节点列表
    def find_node(self, label, properties = {}):
        if isinstance(properties, dict):
            nodes = self.node_matcher.match(label).where(**properties)
        elif isinstance(properties, str): # TODO: 模糊匹配
            # node_matcher.match("Person").where("_.work =~ '月亮.*'")
            # node_matcher.match("Person").where("_.age > 20")
            nodes = self.node_matcher.match(label).where(properties)
        else:
            sys.stderr.write('Error type of properties: expect dict or str, got', type(properties))
        return list(nodes)

    # 查找图谱中存在的节点，返回第一个匹配的节点，不存在则返回None
    def find_one_node(self, label, properties = {}):
        if isinstance(properties, dict):
            nodes = self.node_matcher.match(label).where(**properties)
        elif isinstance(properties, str): # 模糊匹配
            nodes = self.node_matcher.match(label).where(properties)
        else:
            sys.stderr.write('Error type of properties: expect dict or str, got', type(properties))
            return None
        return nodes.first() # 第一个匹配节点，无匹配则为None
    
    def change_node_name(self, label, name, new_name):
        nodes = self.find_node(label, {'name': name})
        for node in nodes:
            node['name'] = new_name
            self.graph.push(node)

    # Property
    # 获取节点的所有属性
    def get_node_properties(self, label, properties):
        nodes = self.find_node(self, label, properties)
        if len(nodes) == 0:
            return {}
        else:
            return dict(nodes[0].items()) # {'name': 'c'}

    # 更新图谱中节点或关系的属性
    def update_properties(graph, node, properties):
        for key in properties:
            node[key] = properties[key]
        graph.push(node)

    # 更新图谱中节点的属性
    # TODO: 删除旧属性？
    def update_property(self, label, properties, new_property):
        node
        node = self.find_one_node(label, properties)
        for key in new_property:
            node[key] = new_property[key]
        self.graph.push(node)

    # Relation
    # 向图谱中的两个节点添加关系
    def add_relation(self, node1, node2, relation, properties = {}):
        edge = Relationship(node1, relation, node2, **properties)
        self.graph.create(edge)
        return edge

    # 查询图谱中两个节点间的关系
    def find_relation(self, nodes = None, relation = None, properties = {}, limit = 10):
        relations = list(self.rel_matcher.match(nodes, r_type = relation).limit(limit))
        return relations

    # change relation name
    # self.change_relation_name('Instanceof', 'Category')
    def change_relation_name(self, relation, new_relation):
        cypher = '''
            MATCH (n1)-[old:{}]->(n2)
            CREATE (n1)-[new:{}]->(n2)
            DELETE old
        '''.format(relation, new_relation)
        self.graph.run(cypher)

    # n1->n2 to n2->n1
    def change_relation_direction(self, relation):
        cypher = '''
            MATCH (n1)-[old:{}]->(n2)
            CREATE (n2)-[new:{}]->(n1)
            DELETE old
        '''.format(relation, relation)
        self.graph.run(cypher)
    
    def del_relation_by_name(self, relation):
        cypher = '''
            MATCH (n1)-[old:{}]->(n2)
            DELETE old
        '''.format(relation)
        self.graph.run(cypher)

    # 解析关系对象Relationship
    def parse_relation(self, relation):
        '''
        {
            '_Walkable__sequence': (Node('食品安全本体', name='产品分类', ontologyid=1), 包括(产品分类)(Node('食品安全本体', name='产品分类', ontologyid=1), Node('产品分类', name='肉制品', proclassid=19)), Node('产品分类', name='肉制品', proclassid=19)), 
            '_Subgraph__nodes': frozenset({Node('产品分类', name='肉制品', proclassid=19), Node('食品安全本体', name='产品分类', ontologyid=1)}), 
            '_Subgraph__relationships': frozenset({包括(产品分类)(Node('食品安全本体', name='产品分类', ontologyid=1), Node('产品分类', name='肉制品', proclassid=19))}), 
            '__uuid__': '2ef66ba9-a55e-4fa9-9d51-d931baaeefbb', 
            '_stale': set(), '_graph': Graph('http://101.6.69.148:7474'), 
            'identity': 32658
        }
        '''
        head = relation.start_node
        tail = relation.end_node
        rel = type(relation).__name__
        triple_id = relation.identity
        # prop = relation.keys()
        # value = relation.get(key)
        return head, tail, rel, triple_id # (_5312:Entity {name: '\u989c\u8272'}) (_6:Product {name: '\u82b1\u751f'}) Target

    def parse_record(self, record):
        relation = record.get('r') # (颜色)-[:Target {}]->(花生)
        if isinstance(relation, list):
            return [self.parse_relation(r) for r in relation]
        return self.parse_relation(relation)

    # 查询一个节点的所有输出关系
    # find_all_relation(graph, node)
    def find_all_relation(self, node):
        # relations = list(self.rel_matcher.match([node], r_type=None)) # r_type = None表示任何类型的关系均可
        relations = list(self.graph.match([node], r_type=None))
        return relations

    # 查询一个节点的所有输入输出关系
    def find_all_bidirectional_relation(self, label, properties):
        relations = self.graph.run('MATCH ()-[r]-(a:' + label + '{name:\'' + properties['name'] + '\'}) RETURN r')
        return relations # Record

    # 查询一个节点的所有输入关系
    def find_all_input_relation(self, label, properties):
        relations = self.graph.run('MATCH ()-[r]->(a:' + label + '{name:\'' + properties['name'] + '\'}) RETURN r')
        return relations # Record

    # others
    def connect_graph(self, host = 'http://localhost:7474', auth = ('neo4j', 'neo4j')):
        self.graph = Graph(host, auth=auth)
        return self.graph

    def del_all_nodes(self):
        self.graph.delete_all()

# entity, opinion, polarity, product, star, category, date, labeled
class ProductGraph(Neo4jGraph):
    def __init__(self, host='http://localhost:7474', auth=('neo4j', 'neo4j')):
        super().__init__(host, auth)
        # self.label_list = ['Entity', 'Opinion', 'Product', 'Category']
        self.label_list = ['产品', '评价对象', '评价词', '评价类别', '情感极性']
        self.polarity_dict = {'POS': '正面', 'NEU': '中性', 'NEG': '负面'}

    def _init_polar(self):
        for polar in self.polarity_dict:
            self.add_entity('Polarity', self.polarity_dict[polar])

    # 没有指定实体类型
    def find_all_entity(self, name):
        nodes = []
        for label in self.label_list:
            node = self.find_node(label, {'name': name})
            nodes += node
        return nodes

    def find_entity(self, label, name):
        nodes = self.find_node(label, {'name': name})
        return nodes
    
    def add_entity(self, label, name):
        return self.add_node(label, {'name': name})
        
    # 查询一个实体节点的所有三元组
    def find_entity_triplet(self, name):
        node = self.get_node('Entity', {'name': name})
        relations = self.find_all_relation(node) # [Category(Node('Entity', name='花生'), Node('Category', name='其它')),...]
        in_relations = self.find_all_input_relation(node)
        return relations + in_relations
    
    def getTriples(self, head, tail, relation):
        nodes = []
        if head is not None:
            node1 = self.find_all_entity(head)
            if node1 == []:
                return []
            nodes.append(node1[0])
        if tail is not None:
            node2 = self.find_all_entity(tail)
            if node2 == []:
                return []
            nodes.append(node2[0])
        triples = self.find_relation(nodes, relation)
        triples = list(map(self.parse_relation, triples))
        return triples

    def getTriples2(self, node1_name, node1_label, node2_name, node2_label, relation):
        nodes = []
        if node1_name is not None:
            if node1_label is None:
                node1 = self.find_all_entity(node1_name)
            else:
                node1 = self.find_entity(node1_name, node1_label)
            if node1 == []:
                return []
            nodes.append(node1[0])
        if node2_name is not None:
            if node2_label is None:
                node2 = self.find_all_entity(node2_name)
            else:
                node2 = self.find_entity(node2_name, node2_label)
            if node2 == []:
                return []
            nodes.append(node2[0])
        
        # 输入关系
        if node1_name is None and node2_name is not None: 
            triples = self.find_all_input_relation(node2_label, {'name': node2_name})
            triples = list(map(self.parse_record, triples))
            if relation is not None:
                triples = [t for t in triples if t[2] == relation]
        else:
            triples = self.find_relation(nodes, relation)
            triples = list(map(self.parse_relation, triples))
        return triples
    
    # add a single item
    def add_data(self, target, opinion, polarity, product, category):
        node_target = self.add_node('Target', {'name': target, 'category': category})
        node_opinion = self.add_node('Opinion', {'name': opinion, 'polarity': polarity, 'category': category})
        node_product = self.add_node('Product', {'name': product})
        node_category = self.add_node('Category', {'name': category})
        polarity = self.polarity_dict[polarity]
        node_polarity = self.find_entity('Polarity', polarity)[0]
        self.add_relation(node_product, node_target, '评价产品')
        self.add_relation(node_product, node_opinion, '产品评价词')
        self.add_relation(node_target, node_opinion, '评价')
        self.add_relation(node_category, node_target, '评价类别') # 类别包含的评价对象
        self.add_relation(node_category, node_opinion, '类别评价词') # 类别对应评价词
        self.add_relation(node_polarity, node_opinion, '评价极性')
        return True

# create Cypher query
class Cypher(ProductGraph):
    def __init__(self, host='http://localhost:7474', auth=('neo4j', 'neo4j')):
        super().__init__(host, auth)




# match (h:Entity {name: '速度'})-[r*1..3]->(m) return h,r,m limit 20

if __name__ == '__main__':
    graph = ProductGraph()
    graph.change_relation_name('Comment', '评价')
    # node = graph.get_node('Product', {'name': '花生'})
    # print(node.get('name'))
    # rel = graph.find_all_input_relation('Product', {'name': '花生'})
    # for r in rel:
    #     graph.parse_record(r)
    #     break
    
    # print(node.items()) # dict_items([('name', 'alice')])
    # graph.find_one_node('Person', {'name': 'alice'})
    # graph = Graph('http://localhost:7474', name='neo4j', password='ngn5110') # Workstation
    # graph = Graph('http://localhost:7474', auth=('neo4j', 'neo4j')) # Cloud
    
    # add_node
    # node = Node('Person', name = 'alice')
    # add_node(graph, 'Person', {'name': 'alice'})
    # graph.add_node('Person', {'name': 'alice'})

    # graph.graph.create_unique
    # add_node(graph, 'Person', {'name': 'alice'})
    # add_node(graph, 'Person', {'name': 'bob'})
    
    # # add relation
    # node1 = graph.find_one_node('Product', {'name': '洋芋'})
    # node2 = graph.find_one_node('Entity', {'name': '薯片'})
    # print(node1, node2)
    # rel = graph.find_relation([node1, node2])
    # print(rel)
    # rel = graph.find_relation([node2, node1])
    # print(rel)
    # rel = graph.find_relation(relation = 'Targetff')
    # node1 = find_node(graph, 'Person', {'name': 'alice'})[0]
    # print(node1)
    # node2 = find_node(graph, 'Person', {'name': '薯片'})[0]
    # print(graph.match([node1]).first())
    # add_relation(graph, node1, 'KNOWS', node2)
    # update_node_prop(graph, node1, {'gender': 'female'})
    # rel = find_relation(graph, [node1])
    # rel = find_relation(graph, [node1, node2])
    # rel = find_relation(graph, relation = 'KNOWS')

