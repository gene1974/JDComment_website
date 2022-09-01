import json
import re


def process_data():
    filepath = './jingdong_comment_830.json'
    from_file = open(filepath, "r", encoding="utf-8")
    from_data = json.load(from_file)
    from_file.close()

    # filepath = './comment_data_unlabeled.json'
    # from_file1 = open(filepath, "r", encoding="utf-8")
    # from_data1 = json.load(from_file1)
    # from_file1.close()
    # for i, data in enumerate(from_data1):
    #     data['date'] = from_data['RECORDS'][data['comment_id']-1]['createTime']
    #     from_data1[i] = data
    
    # filepath = './comment_data_unlabeled.json'
    # to_file = open(filepath, "w", encoding="utf-8")
    # to_file.write(json.dumps(from_data1, ensure_ascii=False, indent=2))
    # to_file.close()

    filepath = './comment_data_labeled.json'
    from_file1 = open(filepath, "r", encoding="utf-8")
    from_data1 = json.load(from_file1)
    from_file1.close()
    for i, data in enumerate(from_data1):
        data['date'] = from_data['RECORDS'][data['comment_id']-1]['createTime']
        from_data1[i] = data
    
    filepath = './nongchanpin.json'
    to_file = open(filepath, "w", encoding="utf-8")
    to_file.write(json.dumps(from_data1, ensure_ascii=False, indent=2))
    to_file.close()
    # print(len(data['RECORDS']))
    # print(data['RECORDS'][1000299 - 1])
    # for line in from_file:
    #     data_list.append(json.loads(line.strip()))
    # from_file.close()

    # to_file_path = "./nongchanpin.json"
    # to_file =  open(to_file_path, "w", encoding="utf-8")
    # to_file.write(json.dumps(data_list, ensure_ascii=False, indent=2))
    # to_file.close()

import argparse

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--filepath', type=str)
    # args = parser.parse_args()
    # print('start data processing %s'%args.filepath)
    process_data()