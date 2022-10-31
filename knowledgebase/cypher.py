import sys
from py2neo import Graph, Node, Relationship
from py2neo import NodeMatcher,RelationshipMatcher


# 用label表示图谱类型：Product

class NodeObject(object):
    def __init__(self, label, name, properties) -> None:
        self.label = label
        self.name = name
        self.properties = properties
        self.node = None

class Neo4jGraph(object):
    def __init__(self, host = 'http://localhost:7474', auth = ('neo4j', 'neo4j')):
        self.host = host
        self.auth = auth
        self.graph = Graph(host, auth = auth)
        self.node_matcher = NodeMatcher(self.graph)
        self.rel_matcher = RelationshipMatcher(self.graph)


    # Nodes
    '''
    @func:  添加一个节点，会重复添加
    @usage: add_node(graph, 'Person', {'name': 'bob'})
    '''
    def add_node(self, label, properties = {}):
        node = self.find_one_node(label, properties)
        if node is None:
            node  = Node(label, **properties)
            self.graph.create(node)
        return node

    '''
    @func:  查找图谱中存在的节点，返回匹配节点列表
    @usage: find_node(graph, 'Person', {'name': 'bob'})
    '''
    def find_node(self, label, properties = {}):
        node_matcher = NodeMatcher(graph)
        if isinstance(properties, dict):
            nodes = node_matcher.match(label).where(**properties)
        elif isinstance(properties, str): # TODO: 模糊匹配
            # node_matcher.match("Person").where("_.work =~ '月亮.*'")
            # node_matcher.match("Person").where("_.age > 20")
            nodes = node_matcher.match(label).where(properties)
        else:
            sys.stderr.write('Error type of properties: expect dict or str, got', type(properties))
        return list(nodes)

    '''
    @func:  查找图谱中存在的节点，返回第一个匹配的节点，不存在则返回None
    @usage: find_node(graph, 'Person', {'name': 'bob'})
    '''
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

    '''
    @func:  返回节点是否存在
    @usage: exist_node(graph, 'Person', {'name': 'bob'})
    '''
    def exist_node(self, label, properties = {}):
        nodes = self.find_node(self, label, properties)
        # return len(nodes) != 0
        if len(nodes) != 0:
            return nodes[0]
        else:
            return False

    # Property
    '''
    @func:  获取图谱中节点的所有属性
    @usage: prop = get_node_properties(graph, 'Person', {'name': 'bob'})
    '''
    def get_node_properties(self, label, properties):
        nodes = self.find_node(self, label, properties)
        if len(nodes) == 0:
            return {}
        else:
            return dict(nodes[0].items()) # {'name': 'c'}

    '''
    @func:  用property中的属性值更新图谱中节点或关系的属性
    @usage: node1 = find_node(graph, 'Person', {'name': 'alice'})[0]
            update_node_prop(graph, node1, {'gender': 'female'})
    @hint:  需要先找到对应节点node
    '''
    def update_properties(graph, node, properties):
        for key in properties:
            node[key] = properties[key]
        graph.push(node)

    def update_property(self, label, properties, new_property):
        node = self.find_one_node(label, properties)
        for key in new_property:
            node[key] = new_property[key]
        self.graph.push(node) # 更新节点？

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
        relations = list(self.rel_matcher.match([node1, node2]))
        print(relations)
        # self.graph.create(edge)

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

    '''
    @func:  解析关系对象Relationship
    @usage: node1 = find_node(graph, 'Person', {'name': 'alice'})[0]
            node2 = find_node(graph, 'Person', {'name': 'bob'})[0]
            relation = find_relation(graph, [node1]) # node1的所有关系
            relation = find_relation(graph, [node1, node2]) # node1到node2的所有关系
            relation = find_relation(graph, relation = 'KNOWS') # 关系为'KNOWS'的所有关系
    '''
    def parse_relation(relation):
        print(relation)
        head = relation.start_node
        tail = relation.end_node
        rel = type(relation).__name__
        prop = relation.keys()
        # value = relation.get(key)
        return head, tail, rel

    '''
    @func:  查询一个节点的所有关系
    @usage: node1 = find_node(graph, 'Person', {'name': 'alice'})[0]
            find_all_relation(graph, node)
    '''
    def find_all_relation(self, node):
        rel_matcher = RelationshipMatcher(self.graph)
        relations = list(rel_matcher.match([node], r_type=None)) # r_type = None表示任何类型的关系均可
        return relations

    '''
    @func:  连接图谱
    @usage: get_graph()
            get_graph(host = 'http://localhost:7474', auth = ('neo4j', 'neo4j'))
    @return graph
    '''
    def connect_graph(self, host = 'http://localhost:7474', auth = ('neo4j', 'neo4j')):
        self.graph = Graph(host, auth=auth)
        return self.graph

    '''
    @func:  删除图谱中的所有节点和关系
    @usage: del_all_nodes(graph)
    '''
    def del_all_nodes(self):
        self.graph.delete_all()

# entity, opinion, polarity, product, star, category, date, labeled
class ProductGraph(Neo4jGraph):
    def __init__(self, host='http://localhost:7474', auth=('neo4j', 'neo4j')):
        super().__init__(host, auth)
        self.graph.schema.create_uniqueness_constraint('Entity', 'Opinion', 'Product', 'Category')

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
    
    def add_eo_relation(self, name):
        return self.add_node('Entity', {'name': name})
    
    # add a single item
    def add_data(self, entity, opinion, polarity, product, category):
        node_target = self.add_node('Entity', {'name': entity})
        node_opinion = self.add_node('Opinion', {'name': opinion, 'polarity': polarity})
        node_product = self.add_node('Product', {'name': product})
        node_category = self.add_node('Category', {'name': category})
        self.add_relation(node_opinion, node_target, 'Comment')     # 评价词->评价对象: Comment
        self.add_relation(node_target, node_product, 'Target')      # 评价对象->产品: Target
        self.add_relation(node_target, node_category, 'Category') # 评价对象->评价类别: Category
        return True

    def add_constrain(self):
        self.graph.schema.create_uniqueness_constraint('person', 'email')



if __name__ == '__main__':
    graph = ProductGraph()
    graph.change_relation_name('Instanceof', 'Category')
    node = Node('Person', name = 'alice')
    # print(node)
    # print(node.items()) # dict_items([('name', 'alice')])
    # graph.find_one_node('Person', {'name': 'alice'})
    # graph = Graph('http://localhost:7474', name='neo4j', password='ngn5110') # Workstation
    # graph = Graph('http://localhost:7474', auth=('neo4j', 'neo4j')) # Cloud
    
    # add_node
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

