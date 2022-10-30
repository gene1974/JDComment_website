import itertools
import json

# get data from original data file, write to 'labeled_data.txt'

def clean_str(text):
    return text.strip().replace('.', '').replace(',', '').replace('，', '').replace('。', '').replace('、', '').replace('：', '').replace('！', '').replace('#', '').replace('*', '')


# {'comment_id': 242153, 'comment_text': '不是被芯6斤，是总重量六斤感觉被坑了', 'comment_variety': '棉花', 'user_star': '3', 'taskNum': '0', 'tag': {'isValue': '0', 'valueList': [{'attribute': 5, 'entity': [{'end': 11, 'start': 8, 'str': '总重量'}], 'evaluation': [{'end': 13, 'start': 11, 'str': '六斤'}], 'polarity': '2'}, {'attribute': '8', 'entity': [], 'evaluation': [{'end': 18, 'start': 13, 'str': '感觉被坑了'}], 'polarity': 0}]}, 'date': '2018-12-26 14:44:39'}

'''
@func get labeled data to triplet
@data 
data = {
    'comment_id': 242153, 
    'comment_text': '不是被芯6斤，是总重量六斤感觉被坑了', 
    'comment_variety': '棉花', 
    'user_star': '3', 
    'taskNum': '0', 
    'tag': {
        'isValue': '0', 
        'valueList': [{
            'attribute': 5, 
            'entity': [{'end': 11, 'start': 8, 'str': '总重量'}], 
            'evaluation': [{'end': 13, 'start': 11, 'str': '六斤'}], 
            'polarity': '2'}, 
            {'attribute': '8', 'entity': [], 'evaluation': [{'end': 18, 'start': 13, 'str': '感觉被坑了'}], 'polarity': 0}
        ]}, 
    'date': '2018-12-26 14:44:39'
}
@out 'labeled_data.txt'
'''
def get_commented_data():
    data = json.load(open('backend/app/data/event/comment_data_labeled.json', 'r'))
    category_list = ['价格','品质','色泽','口感','包装','分量','物流','售后', '其它']
    polar_dict = {0: 'NEG', 1: 'POS', 2: 'NEU'}
    knowledge_base = [] # 11624
    for item in data:
        product = item['comment_variety']
        star = item['user_star']
        date = item['date'] if 'date' in item else ''
        for value in item['tag']['valueList']:
            category = category_list[int(value['attribute'])]
            entities = value['entity']
            comments = value['evaluation']
            polarity = polar_dict[int(value['polarity'])]
            for com in comments:
                com = clean_str(com['str'])
                for ent in entities:
                    ent = clean_str(ent['str'])
                    if ent == '' or com == '':
                        continue
                    # knowledge_base.append({
                    #     'aspect': ent,
                    #     'opinion': com,
                    #     'polarity': ,
                    #     'product': product,
                    #     'star': star,
                    #     'category': category,
                    #     'date': date,
                    #     'labeled': 'labeled', # 是标注数据
                    # })
                    knowledge_base.append(
                        [ent, com, polarity, product, star, category, date, 'labeled']
                    )

    knowledge_base.sort(key = lambda x: x[0])
    with open('./labeled_data.txt', 'w') as f:
        for item in knowledge_base:
            f.write('\t'.join(item) + '\n')

    print('labeled data:', len(knowledge_base))
    return knowledge_base

'''
@func get unlabeled data to triplet
@data 
data = {
    'commentSenti': '好评', 
    'comment_id': 1, 
    'comment_variety': '花生', 
    'user_star': '5', 
    'comment_text': '味道不错，还是会继续回购的，好吃好吃，和豆子大米混在一起熬出来的粥很香，口感好。店里的藜麦卖的很新鲜，快递也是很快的，大家可以放心购买的哈，确实不错，打字好累藜麦营养确实很好，', 
    'date': '2021-08-29 13:31'}
result = {
    'tgt_labels': [(1, 3, '口感', 'POS'), (37, 39, '口感', 'POS')], 
    'opn_labels': [(3, 5, '口感', 'POS'), (15, 17, '口感', 'POS'), (15, 18, '口感', 'POS'), (16, 19, '口感', 'POS'), (15, 19, '口感', 'POS')], 
    'rel_labels': [(1, 3, 3, 5, '口感', 'POS')], 
    'comment_units': [(0, 2, 2, 4, '口感', 'POS'), (36, 38, None, None, '口感', 'POS'), (None, None, 14, 16, '口感', 'POS'), (None, None, 14, 17, '口感', 'POS'), (None, None, 15, 18, '口感', 'POS'), (None, None, 14, 18, '口感', 'POS')]}
'''
def get_example(filename, model):
    data = json.load(open(filename, 'r'))
    knowledge_base = []

    result = model.infer(data[: 2000])
    for data_item, result_item in zip(data, result):
        # 使用ent,opn组装三元组，不使用直接抽取出的四元组
        for ent, opn in itertools.product(result_item['tgt_labels'], result_item['opn_labels']):
            knowledge_base.append({
                'aspect': clean_str(data_item['comment_text'][ent[0] - 1: ent[1] - 1]),
                'opinion': clean_str(data_item['comment_text'][opn[0] - 1: opn[1] - 1]),
                'polarity': opn[3]
            })

    knowledge_base.sort(key = lambda x: (x['aspect'], x['opinion']))
    with open('./unlabeled_triplet_example.txt', 'w') as f:
        for item in knowledge_base:
            f.write(item['aspect'] + '\t' + item['opinion'] + '\t' + item['polarity'] + '\n')
    return knowledge_base

def get_uncommented_data(filename, model):
    data = json.load(open(filename, 'r'))
    knowledge_base = []

    # 循环推断结果，每次推断2000条
    begin, end = 0, 2000
    while begin < len(data):
        result = model.infer(data[begin: end])
        for data_item, result_item in zip(data, result):
            # 使用ent,opn组装三元组，不使用直接抽取出的四元组
            for ent, opn in itertools.product(result_item['tgt_labels'], result_item['opn_labels']):
                ent_text = clean_str(data_item['comment_text'][ent[0] - 1: ent[1] - 1])
                opn_text = clean_str(data_item['comment_text'][opn[0] - 1: opn[1] - 1])
                if ent_text == '' or opn_text == '':
                    continue
                knowledge_base.append({
                    'aspect': ent_text,
                    'opinion': opn_text,
                    'polarity': opn[3]
                })
        begin += 2000
        end += 2000

    # 数量太大不排序，后续改成MySQL存储
    # knowledge_base.sort(key = lambda x: (x['aspect'], x['opinion']))
    print('triplets from unlabeled_data: ', len(knowledge_base))
    with open('./unlabeled_triplet.txt', 'w') as f:
        for item in knowledge_base:
            f.write(item['aspect'] + '\t' + item['opinion'] + '\t' + item['polarity'] + '\n')

    return knowledge_base

if __name__ == '__main__':
    get_commented_data() # 8676
    
    # model
    # args = get_default_args(root + 'backend/app/lib/JDComment')
    # model = Factory(args)
    # model.initialize()
    # get_uncommented_data('allComment.json', model)
