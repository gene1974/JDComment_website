import json
import re

def get_data(filename):
    from_data = json.load(open(filename, "r", encoding="utf-8"))
    print('get raw data: ', len(from_data['RECORDS']))
    return from_data

def dump_data():
    from_data = get_data('./jingdong_comment_830.json')

    to_data = []
    for i in range(len(from_data['RECORDS'])):
        if i%250 == 0:
            # print(i)
            from_data['RECORDS'][i]['comment_id'] = i+1
            from_data['RECORDS'][i]['comment_variety'] = from_data['RECORDS'][i].pop('commentVariety')
            from_data['RECORDS'][i]['user_star'] = from_data['RECORDS'][i].pop('userStar')
            from_data['RECORDS'][i]['comment_text'] = from_data['RECORDS'][i].pop('commentText')
            from_data['RECORDS'][i]['date'] = from_data['RECORDS'][i].pop('createTime')
            to_data.append(from_data['RECORDS'][i])
    
    print('dump new data: ', len(to_data))
    filepath = './newComment.json'
    to_file = open(filepath, "w", encoding="utf-8")
    to_file.write(json.dumps(to_data, ensure_ascii=False, indent=2))
    to_file.close()

def process_data():
    # new data path
    rawfilepath = './jingdong_comment_830.json'
    from_file = open(rawfilepath, "r", encoding="utf-8")
    from_data = json.load(from_file)
    from_file.close()

    to_data = []

    for i in range(len(from_data['RECORDS'])):
        if i%250 == 0:
            # print(i)
            from_data['RECORDS'][i]['comment_id'] = i+1
            from_data['RECORDS'][i]['comment_variety'] = from_data['RECORDS'][i].pop('commentVariety')
            from_data['RECORDS'][i]['user_star'] = from_data['RECORDS'][i].pop('userStar')
            from_data['RECORDS'][i]['comment_text'] = from_data['RECORDS'][i].pop('commentText')
            from_data['RECORDS'][i]['date'] = from_data['RECORDS'][i].pop('createTime')
            to_data.append(from_data['RECORDS'][i])
        
    
    print(len(to_data))
    filepath = './newComment.json'
    to_file = open(filepath, "w", encoding="utf-8")
    to_file.write(json.dumps(to_data, ensure_ascii=False, indent=2))
    to_file.close()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--filepath', type=str)
    # args = parser.parse_args()
    # print('start data processing %s'%args.filepath)
    # process_data()
    dump_data()