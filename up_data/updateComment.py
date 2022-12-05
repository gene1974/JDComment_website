import json
import re

def get_raw_data(filename):
    from_data = json.load(open(filename, "r", encoding="utf-8"))
    print('get raw data: ', len(from_data['RECORDS']))
    return from_data

def add_data(new_file, downsample = 1, old_file = '../backend/app/data/event/newComment.json'):
    old_data = json.load(open(old_file, 'r'))
    print('old data: ', len(old_data))

    raw_data = get_raw_data(new_file)

    for i in range(len(raw_data['RECORDS'])):
        if i%downsample == 0:
            # print(i)
            raw_data['RECORDS'][i]['comment_id'] = i+1
            raw_data['RECORDS'][i]['comment_variety'] = raw_data['RECORDS'][i].pop('commentVariety')
            raw_data['RECORDS'][i]['user_star'] = raw_data['RECORDS'][i].pop('userStar')
            raw_data['RECORDS'][i]['comment_text'] = raw_data['RECORDS'][i].pop('commentText')
            raw_data['RECORDS'][i]['date'] = raw_data['RECORDS'][i].pop('createTime')
            old_data.append(raw_data['RECORDS'][i])
    json.dump(old_data, open(old_file, 'w'))
    print('new data: ', len(old_data))
    

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
    add_data('./comment1125.json', 1)