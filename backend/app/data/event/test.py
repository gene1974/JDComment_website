import datetime
import json
import time

# 筛选新的评论
data = json.load(open('jingdong_comment_830.json', 'r'))
new_data = []
time1 = time.strptime('2022-06-01', "%Y-%m-%d")
for item in data['RECORDS']:
    if time.strptime(item['createTime'][:10], '%Y-%m-%d') > time1:
        new_data.append(item)
print(len(new_data))
json.dump(new_data, open('new_data.json', 'w'))

# 查看新的评论包含的农产品
var_set = set()
data = json.load(open('new_data.json', 'r'))
for item in data:
    var_set.add(item['commentVariety'])
print(var_set)

# f = open('new_data.json', 'r')
# s = f.readline()
# s = s.encode('utf-8').decode('unicode_escape')
# f.close()
# f = open('1.json', 'w')
# f.write(s)
# f.close()
