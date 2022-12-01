import sys
from unicodedata import bidirectional
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


    # Nodes
    # 添加一个节点，更新节点属性；不会重复添加；
    # self.add_node('Person', {'name': 'bob'})
    def add_node(self, label, properties = {}):
        if 'name' not in properties:
            sys.stderr.write('Property `name` is required, get:', properties)
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
    
    def change_node_label(self, label, new_label):
        pass
    
    def change_node_name(self, label, name, new_name):
        nodes = self.find_node(label, {'name': name})
        for node in nodes:
            node['name'] = new_name
            self.graph.push(node)

    # 返回节点是否存在，存在则返回节点
    # TODO: Archived：可以被get_data代替
    def exist_node(self, label, properties = {}):
        nodes = self.find_node(self, label, properties)
        # return len(nodes) != 0
        if len(nodes) != 0:
            return nodes[0]
        else:
            return False

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
    '''
    @func:  向图谱中的两个节点添加关系
    @usage: node1 = find_node(graph, 'Person', {'name': 'alice'})[0]
            node2 = find_node(graph, 'Person', {'name': 'bob'})[0]
            add_relation(graph, node1, 'KNOWS', node2)
    @hint:  两个节点之间可以存在多个关系
    '''
    def add_relation(self, node1, node2, relation, properties = {}):
        edge = Relationship(node1, relation, node2, **properties)
        self.graph.create(edge)

    '''
    @func:  查询图谱中两个节点间的关系
    @usage: node1 = find_node(graph, 'Person', {'name': 'alice'})[0]
            node2 = find_node(graph, 'Person', {'name': 'bob'})[0]
            relation = find_relation(graph, [node1]) # node1的所有关系
            relation = find_relation(graph, [node1, node2]) # node1到node2的所有关系
            relation = find_relation(graph, relation = 'KNOWS') # 关系为'KNOWS'的所有关系
    '''
    def find_relation(self, nodes = None, relation = None, properties = {}, limit = 10):
        relations = list(self.rel_matcher.match(nodes, r_type = relation).limit(limit))
        return relations

    '''
    @func: change relation name
    @usage: self.change_relation_name('Instanceof', 'Category')
    '''
    def change_relation_name(self, relation, new_relation):
        cypher = '''
            MATCH (n1)-[old:{}]->(n2)
            CREATE (n1)-[new:{}]->(n2)
            DELETE old
        '''.format(relation, new_relation)
        self.graph.run(cypher)

    def update_relation(self, nodes = None, relation = None, properties = {}, limit = 10):
        relations = list(self.rel_matcher.match(nodes, r_type = relation).limit(limit))
        return relations

    # 解析关系对象Relationship
    def parse_relation(self, relation):
        print(relation)
        head = relation.start_node
        tail = relation.end_node
        rel = type(relation).__name__
        prop = relation.keys()
        # value = relation.get(key)
        return head, tail, rel # (_5312:Entity {name: '\u989c\u8272'}) (_6:Product {name: '\u82b1\u751f'}) Target

    def parse_record(self, record):
        relation = record.get('r') # (颜色)-[:Target {}]->(花生)
        return self.parse_relation(relation)

    '''
    @func:  查询一个节点的所有输出关系
    @usage: node1 = find_node(graph, 'Person', {'name': 'alice'})[0]
            find_all_relation(graph, node)
    '''
    def find_all_relation(self, node):
        # relations = list(self.rel_matcher.match([node], r_type=None)) # r_type = None表示任何类型的关系均可
        relations = list(self.graph.match([node], r_type=None))
        return relations

    # 查询一个节点的所有输入关系
    def find_all_input_relation(self, label, properties):
        relations = self.graph.run('MATCH ()-[r]-(a:' + label + '{name:\'' + properties['name'] + '\'}) RETURN r')
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

    def add_entity(self, name, properties):
        return self.add_node('Entity', {'name': name})
        # node  = Node('Entity', {'name': name})

    def exist_entity(self, name):
        return self.exist_node('Entity', {'name': name})
    
    def add_opinion(self, name, polarity = None):
        if polarity is not None:
            return self.add_node('Entity', {'name': name, 'polarity': polarity})
        else:
            return self.add_node('Entity', {'name': name})
    
    # 查询一个实体节点的所有三元组
    def find_entity_triplet(self, name):
        node = self.get_node('Entity', {'name': name})
        relations = self.find_all_relation(node) # [Category(Node('Entity', name='花生'), Node('Category', name='其它')),...]
        in_relations = self.find_all_input_relation(node)
        return relations + in_relations
    
    def add_eo_relation(self, name):
        return self.add_node('Entity', {'name': name})
    
    # add a single item
    def add_data(self, entity, opinion, polarity, product, category):
        node_target = self.add_node('Entity', {'name': entity})
        node_opinion = self.add_node('Opinion', {'name': opinion, 'polarity': polarity})
        node_product = self.add_node('Product', {'name': product})
        node_category = self.add_node('Category', {'name': category})
        self.add_relation(node_target, node_opinion, 'Comment')     # 评价对象->评价词: Comment
        self.add_relation(node_product, node_target, 'Target')      # 产品->评价对象: Target
        self.add_relation(node_product, node_target, 'Product')
        self.add_relation(node_target, node_category, 'Category')   # 评价类别->评价对象: Category
        return True

    def add_constrain(self):
        self.graph.schema.create_uniqueness_constraint('Entity', 'name')
        self.graph.schema.create_uniqueness_constraint('Opinion', 'name')
        self.graph.schema.create_uniqueness_constraint('Product', 'name')
        self.graph.schema.create_uniqueness_constraint('Category', 'name')

# match (h:Entity {name: '速度'})-[r*1..3]->(m) return h,r,m limit 20

if __name__ == '__main__':
    graph = ProductGraph()
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

