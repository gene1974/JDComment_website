import json
import os
import random
from app.lib.config import CONFIG
from app.lib.data_helper import load_json, save_json
from dateutil.parser import parse
import datetime
import copy

class EventManager(object):
    @staticmethod
    def load_event():
        event_all = load_json(CONFIG.event_all)
        event_update = load_json(CONFIG.event_update)
        if os.path.exists(CONFIG.event_labeled):
            event_labeled = load_json(CONFIG.event_labeled)
        else:
            event_labeled = []
        # ids_labeled = set(map(lambda x: x['comment_id'], event_labeled))
        # event_unlabeled = list(filter(lambda x: x['comment_id'] not in ids_labeled, event_all))
        # random.shuffle(event_unlabeled)
        return event_labeled, event_all, event_update

    def __init__(self):
        '''
        event_update: newComment.json
        '''
        self.event_labeled, self.event_all, self.event_update = self.load_event()
        ids_labeled = set(map(lambda x: x['comment_id'], self.event_labeled))
        self.event = {
            '0':{
                'event_unlabeled': list(filter(lambda x: x['comment_id'] not in ids_labeled, self.event_all[:2000])),               #未被取走的数据
                'event_labeled': list(filter(lambda x: x['comment_id'] in  set(map(lambda x: x['comment_id'], self.event_all[:1000])), self.event_labeled)),                    #标注完成的数据
                'event_buffer': []                  #被取走但尚未标注的数据
            },
            '1':{
                'event_unlabeled': list(filter(lambda x: x['comment_id'] not in ids_labeled, self.event_all[2000:4000])),
                'event_labeled': list(filter(lambda x: x['comment_id'] in  set(map(lambda x: x['comment_id'], self.event_all[1000:2000])), self.event_labeled)),
                'event_buffer': []
            },
            '2':{
                'event_unlabeled': list(filter(lambda x: x['comment_id'] not in ids_labeled, self.event_all[4000:6000])),
                'event_labeled': list(filter(lambda x: x['comment_id'] in  set(map(lambda x: x['comment_id'], self.event_all[2000:3000])), self.event_labeled)),
                'event_buffer': []
            },
            '3':{
                'event_unlabeled': list(filter(lambda x: x['comment_id'] not in ids_labeled, self.event_all[6000:8000])),
                'event_labeled': list(filter(lambda x: x['comment_id'] in  set(map(lambda x: x['comment_id'], self.event_all[3000:4000])), self.event_labeled)),
                'event_buffer': []
            },
            '4':{
                'event_unlabeled': list(filter(lambda x: x['comment_id'] not in ids_labeled, self.event_all[8000:10000])),
                'event_labeled': list(filter(lambda x: x['comment_id'] in  set(map(lambda x: x['comment_id'], self.event_all[4000:5000])), self.event_labeled)),
                'event_buffer': []
            },
            '5':{
                'event_unlabeled': list(filter(lambda x: x['comment_id'] not in ids_labeled, self.event_all[10000:12000])),
                'event_labeled': list(filter(lambda x: x['comment_id'] in  set(map(lambda x: x['comment_id'], self.event_all[5000:6000])), self.event_labeled)),
                'event_buffer': []
            },
            '6':{
                'event_unlabeled': list(filter(lambda x: x['comment_id'] not in ids_labeled, self.event_all[12000:14000])),
                'event_labeled': list(filter(lambda x: x['comment_id'] in  set(map(lambda x: x['comment_id'], self.event_all[6000:7000])), self.event_labeled)),
                'event_buffer': []
            },
            '7':{
                'event_unlabeled': list(filter(lambda x: x['comment_id'] not in ids_labeled, self.event_all[14000:16000])),
                'event_labeled': list(filter(lambda x: x['comment_id'] in  set(map(lambda x: x['comment_id'], self.event_all[7000:8000])), self.event_labeled)),
                'event_buffer': []
            },
            '8':{
                'event_unlabeled': list(filter(lambda x: x['comment_id'] not in ids_labeled, self.event_all[16000:])),
                'event_labeled': list(filter(lambda x: x['comment_id'] in  set(map(lambda x: x['comment_id'], self.event_all[8000:])), self.event_labeled)),
                'event_buffer': []
            }
        }
        print(len(self.event_update))

    def save_change(self):
        save_json(self.event_labeled, CONFIG.event_labeled)

    def fetch_event(self, taskNum):
        if len(self.event[taskNum]['event_unlabeled']) == 0:
            self.event[taskNum]['event_unlabeled'] = self.event[taskNum]['event_buffer']
            self.event[taskNum]['event_buffer'] = []
        if len(self.event[taskNum]['event_unlabeled']) == 0:
            return '已经完成标注！'
        target_event =  self.event[taskNum]['event_unlabeled'].pop()
        self.event[taskNum]['event_buffer'].append(target_event)
        return target_event

    def remove_from_buffer(self, news_id, taskNum):
        self.event[taskNum]['event_buffer'] = list(filter(lambda x: x['comment_id'] != news_id, self.event[taskNum]['event_buffer']))

    # 如果已经标注过又重新提交 修改标注数据 如果没有标注过 直接保存
    def post_event(self, news_id, events, taskNum):
        if news_id in [i['comment_id'] for i in self.event_labeled]:
            self.event_labeled = list(filter(lambda x: x['comment_id'] != news_id, self.event_labeled))
        self.event_labeled.append(events)

        if news_id in [i['comment_id'] for i in self.event[taskNum]['event_labeled']]:
            self.event[taskNum]['event_labeled'] = list(filter(lambda x: x['comment_id'] != news_id, self.event[taskNum]['event_labeled']))
        self.event[taskNum]['event_labeled'].append(events)

        self.save_change()
        self.remove_from_buffer(news_id, taskNum)

    def count(self, taskNum):
        return len(self.event[taskNum]['event_labeled']), len(self.event[taskNum]['event_unlabeled']) + len(self.event[taskNum]['event_buffer'])
        # return 1, 2

    def update_event_file(self, file):
        data = load_json(os.path.join(CONFIG.upload_folder, file))
        save_json(data, CONFIG.event_all)
        self.__init__()


    def fetch_history_info(self, taskNum):
        return len(self.event[taskNum]['event_labeled'])

    def fetch_page_history(self,page,pageSize, taskNum):
        if len(self.event[taskNum]['event_labeled']) == 0:
            return []
        if pageSize*page+pageSize > len(self.event[taskNum]['event_labeled']):
            return self.event[taskNum]['event_labeled'][pageSize*page:]
        return self.event[taskNum]['event_labeled'][pageSize*page:pageSize*page+pageSize]
        # return jsonify('success')

    def get_daily_info(self, location, variety, start_date, end_date):
        target_events = list(filter(lambda x: x['comment_variety'] in [variety], self.event_update))
        target_events = list(filter(lambda x: parse(start_date) < parse(x['date']) < parse(end_date), target_events))
        print('number: ', len(target_events))

        step=1
        format="%Y-%m-%d"
        strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
        days = (strptime(end_date, format) - strptime(start_date, format)).days
        date_list = [strftime(strptime(start_date, format) + datetime.timedelta(i), format) for i in range(0, days, step)]
        date_dict = {}
        for i in range(len(date_list)):
            date_dict[date_list[i]] = []
        # 将event按日期归类到 date_dict[date]
        for event in target_events:
            if parse(event['date']).strftime('%Y-%m-%d') in date_dict:
                date_dict[parse(event['date']).strftime('%Y-%m-%d')].append(event)
            else:
                date_dict[parse(event['date']).strftime('%Y-%m-%d')] = [event]
        results = []
        for key in date_dict:
            result = {}
            result['date'] = key
            result['comment_number'] = len(date_dict[key])
            if result['comment_number'] > 0:
                result['average_score'] = float(sum(int(x['user_star']) for x in date_dict[key]))/result['comment_number']
            else:
                result['average_score'] = 0
            result['average_score'] = round(result['average_score'], 2)
            results.append(result)
        return results

    def get_date_info(self, location, variety, start_date, end_date):
        #self.__init__()
        target_events = list(filter(lambda x: x['comment_variety'] in [variety], self.event_update))
        target_events = list(filter(lambda x: parse(start_date) < parse(x['date']) < parse(end_date), target_events))
        return copy.deepcopy(target_events)

    def get_all_product_graph(self):
        attrs = list(range(9))
        self.varietys = list(set(item['comment_variety'] for item in self.event_labeled))
        self.product_comments = {v:{i: [] for i in range(9)} for v in self.varietys}
        name_list = {v: [] for v in self.varietys}
        for comment in self.event_labeled:
            for item in comment['tag']['valueList']:
                if item['attribute'] in attrs and item['entity'] != [] and item['evaluation'] != []:
                    for i in range(len(item['entity'])):
                        ent = item['entity'][i]['str'].replace('.', '').replace(',', '').replace('，', '').replace('。', '').replace('、', '')
                        eva = item['evaluation'][0]['str'].replace('.', '').replace(',', '').replace('，', '').replace('。', '').replace('、', '')
                        if ent not in name_list[comment['comment_variety']]:
                            name_list[comment['comment_variety']].append(ent)
                            self.product_comments[comment['comment_variety']][item['attribute']].append({'name': ent, 'children': [eva]})
        # for variety in self.product_comments:
        #     print(type(variety))
        #     product_comments = []
        #     name_list = []
        #     for node in self.product_comments[variety]:
        #         if node['name'] not in name_list:
        #             product_comments.append(node)
        #     self.product_comments[variety] = product_comments
            # self.product_comments[variety] = self.product_comments[variety][:20]
                # if item['attribute'] not in attrs:
                #     continue
                # if item['entity'] == [] and item['evaluation'] == []:
                #     continue
                # elif item['entity'] == []:
                #     continue
                #     self.product_comments[comment['comment_variety']][item['attribute']].append({'name': '', 'children': [item['evaluation'][0]['str']]})
                # elif item['evaluation'] == []:
                #     continue
                #     self.product_comments[comment['comment_variety']][item['attribute']].append({'name': item['entity'][0]['str'], 'children': ['']})
                # else:
                #     for i in range(len(item['entity'])):
                #         self.product_comments[comment['comment_variety']][item['attribute']].append({'name': item['entity'][i]['str'], 'children': [item['evaluation'][0]['str']]})

    def year_result(self, variety):
        variety_comment_dict = {
            '大米': '''
                消费者对大米整体非常满意，综合评分为4.27。
                总体来说，这段时间内大米价格便宜，包装精美，口感较好，品质较好，售后服务较好，物流较好，色泽较好。''',
            '番茄': '''
                消费者对番茄整体非常满意，综合评分为4.08。
                根据消费者的评价，今年上半年，番茄价格中等，分量中等，包装精美，口感较好，品质较好，物流中等，色泽较好。''',
            '茶叶': '''
                消费者对茶叶整体较为满意，综合评分为3.81。
                根据消费者的评价，今年上半年，茶叶包装精美，口感较好，品质较好。''',
            '荸荠': '''
                消费者对荸荠整体非常满意，综合评分为5.00。
                根据消费者的评价，今年上半年，荸荠物流较好。''',
            '油茶': '''
                油茶没有评价信息。''',
            '猕猴桃': '''
                消费者对猕猴桃整体非常满意，综合评分为4.16。
                根据消费者的评价，今年上半年，猕猴桃价格便宜，分量较少，口感较好，品质中等，物流较好。''',
            '竹笋': '''
                消费者对竹笋整体非常满意，综合评分为4.25。
                根据消费者的评价，今年上半年，竹笋价格便宜，分量较多，包装中等，口感较好，品质较好，物流较好。''',
            '红米': '''
                红米没有评价信息。''',
            '蜜柚': '''
                消费者对蜜柚整体较为满意，综合评分为3.97。
                根据消费者的评价，今年上半年，蜜柚分量较多，包装精美，口感较好，品质较好，物流较差。''',
            '茶油': '''
                消费者对茶油整体非常满意，综合评分为5.00。''',
            '贡米': '''
                贡米没有评价信息。''',
            '炒青': '''
                炒青没有评价信息。''',
            '椪柑': '''
                消费者对椪柑整体较为满意，综合评分为3.17。
                根据消费者的评价，今年上半年，椪柑分量中等，口感较差，品质较好。''',
            '大蒜': '''
                消费者对大蒜整体非常满意，综合评分为4.44。
                根据消费者的评价，今年上半年，大蒜价格便宜，分量较多，包装精美，口感较好，品质较好，物流较好，色泽较好。''',
            '白肉姜': '''
                白肉姜没有评价信息。''',
            '红心脚板薯': '''
                红心脚板薯没有评价信息。''',
            '藕': '''
                消费者对藕整体非常满意，综合评分为4.14。
                根据消费者的评价，今年上半年，藕价格便宜，分量较多，包装精美，口感较好，品质中等，售后服务较好，物流较好。''',
            '酱姜': '''
                酱姜没有评价信息。''',
            '豆皮': '''
                消费者对豆皮整体较为满意，综合评分为3.67。''',
            '橙皮': '''
                橙皮没有评价信息。''',
            '蜜茄': '''
                消费者对蜜茄整体非常满意，综合评分为4.57。
                根据消费者的评价，今年上半年，蜜茄包装精美，物流较好。''',
        }
        comment = '' + variety + '的评价信息：'
        comment += variety_comment_dict[variety]
        return comment
    
    def get_product(self, variety):
        attr_list = ['价格','品质','色泽','口感','包装','分量','物流','售后', '其它']
        if not hasattr(self, 'product_comments'):
            self.get_all_product_graph()
        variety_comments = self.product_comments[variety]
        graph_data = {
            'name': variety,
            'children': [
                {'name': attr_list[i], 'children': variety_comments[i]} for i in range(9)
            ]
        }
        comment_data = self.year_result(variety)
        res = {
            'comment_data': comment_data,
            'graph_data': graph_data
        }
        return res

EVENT = EventManager()
