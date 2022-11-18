import csv
import json
import sys
from py2neo import Graph, Node, Relationship
from py2neo import NodeMatcher,RelationshipMatcher



class Neo4jGraph(object):
    def __init__(self, host = 'http://localhost:7474', auth = ('neo4j', 'neo4j')):
        self.host = host
        self.auth = auth
        self.graph = Graph(host, auth = auth)
        self.node_matcher = NodeMatcher(self.graph)
        self.rel_matcher = RelationshipMatcher(self.graph)

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

    def update_relation(self, nodes = None, relation = None, properties = {}, limit = 10):
        relations = list(self.rel_matcher.match(nodes, r_type = relation).limit(limit))
        return relations

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

class KnowledgeGraph(Neo4jGraph):
    def __init__(self, host='http://localhost:7474', auth=('neo4j', 'neo4j')):
        super().__init__(host, auth)
        self.label_list = ['产品分类', '判定标准', '检验依据', '检验标准', '检验项目', '食品安全本体']
        # self.label_list = ['化学污染物食品分类', '微生物食品分类', '暴发食品分类', '标准属性', '标准分类']

    # 没有指定实体类型
    def find_all_entity(self, name):
        nodes = []
        for label in self.label_list:
            node = self.find_node(label, {'name': name})
            nodes += node
        return nodes


# API
KG = KnowledgeGraph('http://101.6.69.191:7474')

def getTriples(head, tail, relation):
    node1 = KG.find_all_entity(head)[0]
    node2 = KG.find_all_entity(tail)[0]
    nodes = [node1, node2]
    triples = KG.find_relation(nodes, relation)
    triples = list(map(KG.parse_relation, triples))
    return triples

def saveTriple(triple_id, head, tail, relation):
    deleteTriple(triple_id)
    res = addTriple(head, tail, relation)
    return res


def deleteTriple(triple_id):
    try:
        triple = KG.rel_matcher[triple_id]
    except:
        return False
    KG.graph.delete(triple)
    return True

def addTriple(head, tail, relation, need_exist = False):
    exist_h, exist_t, exist_r = True, True, False
    err_msg = ''
    node1 = KG.find_all_entity(head)
    node2 = KG.find_all_entity(tail)
    if node1 == []:
        exist_h = False
        node1 = KG.add_node('新增节点', {'name': head})
        err_msg += '头节点不存在，新增头节点。'
    if node2 == []:
        exist_t = False
        node2 = KG.add_node('新增节点', {'name': tail})
        err_msg += '尾节点不存在，新增尾节点。'
    
    nodes = [node1[0], node2[0]]
    triples = KG.find_relation(nodes, relation)
    if triples != []:
        exist_h = True
        err_msg = '三元组已经存在。'
    else:
        triple = KG.add_relation(node1[0], node2[0], relation)
        triple = KG.parse_relation(triple)
        err_msg = '新增成功。' + err_msg
    
    if need_exist:
        return True, err_msg, triple, exist_h, exist_t, exist_r
    else:
        return True, err_msg, triple

def uploadTriples(triple_filepath):
    succ_num, fail_num = 0, 0
    succ_triples = []
    try:
        reader = csv.reader(open(triple_filepath), 'r')
        for line in reader:
            head, tail, relation = line
            succ, err_msg, triple, exist_h, exist_t, exist_r = addTriple(head, tail, relation, True)
            if succ:
                succ_triples.append({
                    'relation_new': exist_r,
                    'tail_new': exist_t,
                    'head_new': exist_h,
                    'id': triple[3],
                    'head': triple[0],
                    'tail': triple[1],
                    'relation': triple[2],
                    'result': succ,
                    'error': err_msg,
                })
                succ_num += 1
            else:
                fail_num += 1
                succ_triples.append({
                    'relation_new': exist_r,
                    'tail_new': exist_t,
                    'head_new': exist_h,
                    'id': -1,
                    'head': head,
                    'tail': tail,
                    'relation': relation,
                    'result': succ,
                    'error': err_msg,
                })
    except Exception as e:
        sys.stderr.write(e)
    return succ_num, succ_triples


def graphSearch(input):
    nodes = KG.find_all_entity(input)
    if nodes == []:
        return []
    node = nodes[0]
    relations = KG.find_all_relation(node)
    relations = list(map(KG.parse_relation, relations))
    return relations

def graphAdvancedSearch(entity, depth = 1, maximum = 20):
    nodes = KG.find_all_entity(entity)
    if nodes == []:
        return []
    node = nodes[0]
    label = list(node._labels)[0]
    cypher = '''
        match (h:{}{{name: \'{}\'}})-[r*1..{}]->(m) return r limit {}
    '''.format(label, entity, depth, maximum)
    res = KG.graph.run(cypher)
    result = set()
    for record in res:
        # result += KG.parse_record(record)
        result |= set(KG.parse_record(record))
    return list(result)

if __name__ == '__main__':
    # triples = saveTriple(32656, 'a', 'b', 'c')
    # print(triples)

    # res = deleteTriple(32658)
    # res = deleteTriple(10000000)
    # print(res)

    # triples = addTriple('产品分类', '肉制品', '测试关系')
    # print(triples)

    # triples = getTriples('产品分类', '肉制品', '包括(产品分类)')
    # print(triples)

    relations = graphSearch('肉制品')
    print(relations)

    # relations = graphAdvancedSearch('肉制品', 3)
    # print(relations)
