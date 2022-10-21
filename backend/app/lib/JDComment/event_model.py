# -*- coding: utf-8 -*-
import math
from app.lib.JDComment.code.config import get_default_args
from app.lib.JDComment.code.factory import Factory
from ltp import LTP
nlp = LTP()
import json

class EventModel(object):
    def __init__(self):
        self.root = "app/lib/JDComment"  # 项目根目录
        self.args = get_default_args(root=self.root)  # 默认参数
        self.factory = Factory(self.args)
        self.factory.initialize()  # 初始化

    def data_analysis(self, data_list):
        results = self.factory.infer(data_list)
        # print(results)
        resize_results = []
        for i in range (len(data_list)):
            resize_result = {'comment_text': data_list[i]['comment_text']}
            resize_result['comment_units'] = []
            # print(resize_result['comment_text'])
            seg_list, hidden = nlp.seg([resize_result['comment_text']])
            seg_list = seg_list[0]
            seg_word_len_list = [len(word) for word in seg_list]
            seg_head_list = [sum(seg_word_len_list[:i]) for i in range(len(seg_word_len_list))]
            seg_tail_list = [sum(seg_word_len_list[:i+1]) for i in range(len(seg_word_len_list))]
            # print(seg_head_list)
            # print(seg_tail_list)
            for tup in results[i]['comment_units']:
                temp_entity = {}
                temp_evaluation = {}
                # resize_result['comment_units'].append((str(tup[0]), str(tup[1]), str(tup[2]), str(tup[3]), str(tup[4]), str(tup[5])))
                if tup[0] in seg_head_list and tup[1] in seg_tail_list and tup[2] in seg_head_list and tup[3] in seg_tail_list:
                    if (tup[0] == None):
                        temp_entity['text'] = 'NONE'
                        temp_entity['head'] = None
                        temp_entity['tail'] = None
                    else:
                        temp_entity['text'] = resize_result['comment_text'][tup[0]:tup[1]]
                        temp_entity['head'] = str(tup[0])
                        temp_entity['tail'] = str(tup[1])
                    if (tup[2] == None):
                        temp_evaluation['text'] = 'NONE'
                        temp_evaluation['head'] = None
                        temp_evaluation['tail'] = None
                    else:
                        temp_evaluation['text'] = resize_result['comment_text'][tup[2]:tup[3]]
                        temp_evaluation['head'] = str(tup[2])
                        temp_evaluation['tail'] = str(tup[3])
                    
                    resize_result['comment_units'].append({'entity':temp_entity, 'evaluation':temp_evaluation, 'attribute':tup[4], 'polarity':tup[5]})
            resize_results.append(resize_result)
        # print(results)
        return resize_results

    def txt_analysis(self, txt_list):
        # {'commentSenti': '好评', 'comment_id': 2641251, 'comment_variety': '大米', 'user_star': '5', 'comment_text': '大米非常好吃，快递也给力', 'date': '2022-03-02 18:43:17'}
        # data_list = [{'comment_text':item['comment_text']} for item in txt_list]
        # if len(txt_list) < 1:
        #     return []
        # elif len(txt_list) < 50:
        #     results = self.factory.infer(txt_list)
        # else:
        #     results = []
        #     for i in range(math.ceil(len(txt_list)/50) - 1):
        #         results += self.factory.infer(txt_list[i*50: (i+1)*50])
        #     results += self.factory.infer(txt_list[(math.ceil(len(txt_list)/50) - 1)*50: ])
        results = self.factory.infer(txt_list)
        resize_results = []
        statistics_result = {
            "polarity":{},
            "variety":{
            },
        }
        for i in range (len(txt_list)):
            resize_result = txt_list[i]
            if resize_result['comment_variety'] in statistics_result['variety']:
                statistics_result['variety'][resize_result['comment_variety']]['count'] += 1
            else:
                statistics_result['variety'][resize_result['comment_variety']] = {'count':1, 'polarity':{}, 'aspect':{}}
            resize_result['comment_units'] = []
            seg_list, hidden = nlp.seg([resize_result['comment_text']])
            seg_list = seg_list[0]
            seg_word_len_list = [len(word) for word in seg_list]
            seg_head_list = [sum(seg_word_len_list[:i]) for i in range(len(seg_word_len_list))]
            seg_tail_list = [sum(seg_word_len_list[:i+1]) for i in range(len(seg_word_len_list))]
            for tup in results[i]['comment_units']:
                # temp_entity = {}
                # temp_evaluation = {}
                # resize_result['comment_units'].append((str(tup[0]), str(tup[1]), str(tup[2]), str(tup[3]), str(tup[4]), str(tup[5])))
                if tup[0] in seg_head_list and tup[1] in seg_tail_list and tup[2] in seg_head_list and tup[3] in seg_tail_list:
                    resize_result['comment_units'].append({'entity':resize_result['comment_text'][tup[0]:tup[1]] if (tup[0] != None) else 'NONE', 'evaluation':resize_result['comment_text'][tup[2]:tup[3]] if (tup[2] != None) else 'NONE', 'attribute':tup[4], 'polarity':tup[5]})
                    # if (tup[0] == None):
                    #     temp_entity['text'] = 'NONE'
                    #     temp_entity['head'] = None
                    #     temp_entity['tail'] = None
                    # else:
                    #     temp_entity['text'] = resize_result['comment_text'][tup[0]:tup[1]]
                    #     temp_entity['head'] = str(tup[0])
                    #     temp_entity['tail'] = str(tup[1])
                    # if (tup[2] == None):
                    #     temp_evaluation['text'] = 'NONE'
                    #     temp_evaluation['head'] = None
                    #     temp_evaluation['tail'] = None
                    # else:
                    #     temp_evaluation['text'] = resize_result['comment_text'][tup[2]:tup[3]]
                    #     temp_evaluation['head'] = str(tup[2])
                    #     temp_evaluation['tail'] = str(tup[3])
                    # resize_result['comment_units'].append({'entity':temp_entity, 'evaluation':temp_evaluation, 'attribute':tup[4], 'polarity':tup[5]})
                    if resize_result['comment_units'][-1]['polarity'] in statistics_result['polarity']:
                        statistics_result['polarity'][resize_result['comment_units'][-1]['polarity']] += 1
                    else:
                        statistics_result['polarity'][resize_result['comment_units'][-1]['polarity']] = 1

                    if resize_result['comment_units'][-1]['polarity'] in statistics_result['variety'][resize_result['comment_variety']]['polarity']:
                        statistics_result['variety'][resize_result['comment_variety']]['polarity'][resize_result['comment_units'][-1]['polarity']] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['polarity'][resize_result['comment_units'][-1]['polarity']] = 1

                    if resize_result['comment_units'][-1]['attribute'] in statistics_result['variety'][resize_result['comment_variety']]['aspect']:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['count'] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']] = {'count':1, 'polarity':{}, 'target':{}}
                    
                    if resize_result['comment_units'][-1]['polarity'] in statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['polarity']:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['polarity'][resize_result['comment_units'][-1]['polarity']] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['polarity'][resize_result['comment_units'][-1]['polarity']] = 1

                    if resize_result['comment_units'][-1]['entity'] in statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target']:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']]['count'] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']] = {'count':1, 'polarity':{}, 'opinion':{}}
                    
                    if resize_result['comment_units'][-1]['polarity'] in statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']]['polarity']:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']]['polarity'][resize_result['comment_units'][-1]['polarity']] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']]['polarity'][resize_result['comment_units'][-1]['polarity']] = 1
                    
                    if resize_result['comment_units'][-1]['evaluation'] in statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']]['opinion']:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']]['opinion'][resize_result['comment_units'][-1]['evaluation']]['count'] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']]['opinion'][resize_result['comment_units'][-1]['evaluation']] = {'count':1, 'polarity':{}}
                    
                    if resize_result['comment_units'][-1]['polarity'] in statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']]['opinion'][resize_result['comment_units'][-1]['evaluation']]['polarity']:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']]['opinion'][resize_result['comment_units'][-1]['evaluation']]['polarity'][resize_result['comment_units'][-1]['polarity']] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']]['opinion'][resize_result['comment_units'][-1]['evaluation']]['polarity'][resize_result['comment_units'][-1]['polarity']] = 1
                    # continue
            resize_results.append(resize_result)
        # print(results)
        final_results = {}
        final_results['comment_result'] = resize_results
        final_results['statistics_result'] = statistics_result
        # resize_results.append(statistics_result)
        # return resize_results
        # with open('./result.json', mode="w", encoding="utf-8") as file:
        #     file.write(json.dumps(final_results, ensure_ascii=False, indent=5))
        return final_results

    def wenjian_analysis(self, txt_list):
        # data_list = [{'comment_text':item['comment_text']} for item in txt_list]
        # if len(txt_list) < 1:
        #     return []
        # elif len(txt_list) < 50:
        #     results = self.factory.infer(txt_list)
        # else:
        #     results = []
        #     for i in range(math.ceil(len(txt_list)/50) - 1):
        #         results += self.factory.infer(txt_list[i*50: (i+1)*50])
        #     results += self.factory.infer(txt_list[(math.ceil(len(txt_list)/50) - 1)*50: ])
        results = self.factory.infer(txt_list)
        resize_results = []
        statistics_result = {
            "polarity":{},
            "variety":{
            },
        }
        siyuanzu_result = []
        for i in range (len(txt_list)):
            resize_result = txt_list[i]
            if resize_result['comment_variety'] in statistics_result['variety']:
                statistics_result['variety'][resize_result['comment_variety']]['count'] += 1
                statistics_result['variety'][resize_result['comment_variety']]['user_stars'] += int(resize_result['user_star'])
            else:
                statistics_result['variety'][resize_result['comment_variety']] = {'count':1, 'polarity':{}, 'aspect':{}, 'user_stars': 0}
            resize_result['comment_units'] = []
            seg_list, hidden = nlp.seg([resize_result['comment_text']])
            seg_list = seg_list[0]
            seg_word_len_list = [len(word) for word in seg_list]
            seg_head_list = [sum(seg_word_len_list[:i]) for i in range(len(seg_word_len_list))]
            seg_tail_list = [sum(seg_word_len_list[:i+1]) for i in range(len(seg_word_len_list))]
            for tup in results[i]['comment_units']:
                temp_entity = {}
                temp_evaluation = {}
                # resize_result['comment_units'].append((str(tup[0]), str(tup[1]), str(tup[2]), str(tup[3]), str(tup[4]), str(tup[5])))
                if tup[0] in seg_head_list and tup[1] in seg_tail_list and tup[2] in seg_head_list and tup[3] in seg_tail_list:
                    # resize_result['comment_units'].append({'entity':resize_result['comment_text'][tup[0]:tup[1]] if (tup[0] != None) else 'NONE', 'evaluation':resize_result['comment_text'][tup[2]:tup[3]] if (tup[2] != None) else 'NONE', 'attribute':tup[4], 'polarity':tup[5]})
                    if (tup[0] == None):
                        temp_entity['text'] = 'NONE'
                        temp_entity['head'] = None
                        temp_entity['tail'] = None
                    else:
                        temp_entity['text'] = resize_result['comment_text'][tup[0]:tup[1]]
                        temp_entity['head'] = str(tup[0])
                        temp_entity['tail'] = str(tup[1])
                    if (tup[2] == None):
                        temp_evaluation['text'] = 'NONE'
                        temp_evaluation['head'] = None
                        temp_evaluation['tail'] = None
                    else:
                        temp_evaluation['text'] = resize_result['comment_text'][tup[2]:tup[3]]
                        temp_evaluation['head'] = str(tup[2])
                        temp_evaluation['tail'] = str(tup[3])
                    resize_result['comment_units'].append({'entity':temp_entity, 'evaluation':temp_evaluation, 'attribute':tup[4], 'polarity':tup[5]})
                    if resize_result['comment_units'][-1]['polarity'] in statistics_result['polarity']:
                        statistics_result['polarity'][resize_result['comment_units'][-1]['polarity']] += 1
                    else:
                        statistics_result['polarity'][resize_result['comment_units'][-1]['polarity']] = 1

                    if resize_result['comment_units'][-1]['polarity'] in statistics_result['variety'][resize_result['comment_variety']]['polarity']:
                        statistics_result['variety'][resize_result['comment_variety']]['polarity'][resize_result['comment_units'][-1]['polarity']] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['polarity'][resize_result['comment_units'][-1]['polarity']] = 1

                    if resize_result['comment_units'][-1]['attribute'] in statistics_result['variety'][resize_result['comment_variety']]['aspect']:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['count'] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']] = {'count':1, 'polarity':{}, 'target':{}}
                    
                    if resize_result['comment_units'][-1]['polarity'] in statistics_result['variety'][resize_result['comment_variety']]['aspect']\
                    [resize_result['comment_units'][-1]['attribute']]['polarity']:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['polarity']\
                        [resize_result['comment_units'][-1]['polarity']] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['polarity']\
                        [resize_result['comment_units'][-1]['polarity']] = 1

                    if resize_result['comment_units'][-1]['entity']['text'] in statistics_result['variety'][resize_result['comment_variety']]['aspect']\
                    [resize_result['comment_units'][-1]['attribute']]['target']:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target']\
                        [resize_result['comment_units'][-1]['entity']['text']]['count'] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target']\
                        [resize_result['comment_units'][-1]['entity']['text']] = {'count':1, 'polarity':{}, 'opinion':{}}
                    
                    if resize_result['comment_units'][-1]['polarity'] in statistics_result['variety'][resize_result['comment_variety']]['aspect']\
                    [resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']['text']]['polarity']:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target']\
                        [resize_result['comment_units'][-1]['entity']['text']]['polarity'][resize_result['comment_units'][-1]['polarity']] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target']\
                        [resize_result['comment_units'][-1]['entity']['text']]['polarity'][resize_result['comment_units'][-1]['polarity']] = 1
                    
                    if resize_result['comment_units'][-1]['evaluation']['text'] in statistics_result['variety'][resize_result['comment_variety']]['aspect']\
                    [resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']['text']]['opinion']:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target']\
                        [resize_result['comment_units'][-1]['entity']['text']]['opinion'][resize_result['comment_units'][-1]['evaluation']['text']]['count'] += 1
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target']\
                        [resize_result['comment_units'][-1]['entity']['text']]['opinion'][resize_result['comment_units'][-1]['evaluation']['text']] = {'count':1, 'polarity':{}}
                    
                    if resize_result['comment_units'][-1]['polarity'] in statistics_result['variety'][resize_result['comment_variety']]['aspect']\
                    [resize_result['comment_units'][-1]['attribute']]['target'][resize_result['comment_units'][-1]['entity']['text']]['opinion'][resize_result['comment_units'][-1]['evaluation']['text']]['polarity']:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target']\
                        [resize_result['comment_units'][-1]['entity']['text']]['opinion'][resize_result['comment_units'][-1]['evaluation']['text']]['polarity'][resize_result['comment_units'][-1]['polarity']]['count'] += 1
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target']\
                        [resize_result['comment_units'][-1]['entity']['text']]['opinion'][resize_result['comment_units'][-1]['evaluation']['text']]['polarity'][resize_result['comment_units'][-1]['polarity']]['sentence'].append(i)
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target']\
                        [resize_result['comment_units'][-1]['entity']['text']]['opinion'][resize_result['comment_units'][-1]['evaluation']['text']]['polarity'][resize_result['comment_units'][-1]['polarity']]['sentence'] =\
                        list(set(statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target']\
                        [resize_result['comment_units'][-1]['entity']['text']]['opinion'][resize_result['comment_units'][-1]['evaluation']['text']]['polarity'][resize_result['comment_units'][-1]['polarity']]['sentence']))
                    else:
                        statistics_result['variety'][resize_result['comment_variety']]['aspect'][resize_result['comment_units'][-1]['attribute']]['target']\
                        [resize_result['comment_units'][-1]['entity']['text']]['opinion'][resize_result['comment_units'][-1]['evaluation']['text']]['polarity'][resize_result['comment_units'][-1]['polarity']] = {'count':1,'sentence':[i]}
                    # continue
            resize_results.append(resize_result)
        # print(results)
        final_results = {}
        for variety in statistics_result['variety']:
            for aspect in statistics_result['variety'][variety]['aspect']:
                for target in statistics_result['variety'][variety]['aspect'][aspect]['target']:
                    for opinion in statistics_result['variety'][variety]['aspect'][aspect]['target'][target]['opinion']:
                        for polarity in statistics_result['variety'][variety]['aspect'][aspect]['target'][target]['opinion'][opinion]['polarity']:
                            siyuanzu_result.append({'variety':variety, 'aspect': aspect, 'target': target, 'opinion': opinion, 'polarity': polarity,
                            'count': statistics_result['variety'][variety]['aspect'][aspect]['target'][target]['opinion'][opinion]['polarity'][polarity]['count'], 
                            'sentence': statistics_result['variety'][variety]['aspect'][aspect]['target'][target]['opinion'][opinion]['polarity'][polarity]['sentence']})
        siyuanzu_result.sort(key = lambda x :x['count'], reverse = True)
        final_results['comment_result'] = resize_results
        final_results['statistics_result'] = statistics_result
        final_results['siyuanzu_result'] = siyuanzu_result
        # resize_results.append(statistics_result)
        # return resize_results
        # with open('./result.json', mode="w", encoding="utf-8") as file:
        #     file.write(json.dumps(final_results, ensure_ascii=False, indent=5))
        return final_results

EVENTMODEL = EventModel()


# resize_result['comment_units'].append({
#                         'entity':{'text':resize_result['comment_text'][tup[0]:tup[1]], 'head':tup[0], 'tail':tup[1]} if (tup[0] != None) else {'text':'NONE', 'head':None, 'tail':None}, 
#                         'evaluation':{'text':resize_result['comment_text'][tup[2]:tup[3]], 'head':tup[2], 'tail':tup[3]} if (tup[2] != None) else {'text':'NONE', 'head':None, 'tail':None}, 
#                         'attribute':tup[4], 'polarity':tup[5]})