import json

# add data to data_unlabeled

# original_data
data_all = json.load(open('comment_data_unlabeled.json', 'r'))
print('original data: ', len(data_all))

# new_data
data1 = json.load(open('jingdong_comment_830_0815.json', 'r'))
print('new data: ', len(data1['RECORDS']))

item_id = 0
for item in data1['RECORDS']:
    if item_id % 250 == 0:
        data_all.append({
            'comment_id': item_id,
            'comment_variety': item['commentVariety'],
            'user_star': item['userStar'],
            'comment_text': item['commentText'],
            'date': item['createTime'],
        })
    item_id += 1
data_all.sort(key = lambda x: x['comment_id'])
json.dump(data_all, open('comment_data_unlabeled.json', 'w'))
print('final data: ', len(data_all))
