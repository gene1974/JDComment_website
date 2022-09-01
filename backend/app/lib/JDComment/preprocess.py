# -*- coding: utf-8 -*-

import json
import random


def reformat():
    # comment_20211231.json >> comment_labeled.json
    aspect_list = ["价格", "品质", "色泽", "口感", "包装", "分量", "物流", "售后", "其他"]
    polarity_list = ["NEG", "POS", "NEU"]

    file_path = "/data1/chenfang/Project/JDComment/data/comment_20211231.json"
    with open(file_path, mode="r", encoding="utf-8") as file:
        data_list = json.load(file)

    new_data_list = []
    for data in data_list:
        new_data = {
            "comment_id": data["comment_id"],
            "comment_variety": data["comment_variety"],
            "user_star": data["user_star"],
            "comment_text": data["comment_text"],
            "comment_units": [],
        }
        for value in data["tag"]["valueList"]:
            unit = {
                "target": [{"head": x["start"], "tail": x["end"], "text": x["str"]} for x in value["entity"]],
                "opinion": [{"head": x["start"], "tail": x["end"], "text": x["str"]} for x in value["evaluation"]],
                "aspect": aspect_list[int(value["attribute"])],
                "polarity": polarity_list[int(value["polarity"])],
            }
            new_data["comment_units"].append(unit)
        new_data_list.append(new_data)
    new_data_list = sorted(new_data_list, key=lambda x: x["comment_id"], reverse=False)

    file_path = "/data1/chenfang/Project/JDComment/data/comment_labeled.json"
    with open(file_path, mode="w", encoding="utf-8") as file:
        for new_data in new_data_list:
            file.write(json.dumps(new_data, ensure_ascii=False) + "\n")


def filter():
    # comment_labeled.json >> comment_filtered.json
    new_data_list = []
    file_path = "/data1/chenfang/Project/JDComment/data/comment_labeled.json"
    with open(file_path, mode="r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line.strip())
            new_data = {
                "comment_id": data["comment_id"],
                "comment_variety": data["comment_variety"],
                "user_star": data["user_star"],
                "comment_text": data["comment_text"],
                "comment_units": [],
            }
            # 保证对象和观点只对应一个连续的文本片段
            for unit in data["comment_units"]:
                num_tgt_segs = len(unit["target"])
                num_opn_segs = len(unit["opinion"])
                if (num_tgt_segs == 1) and (num_opn_segs == 1):
                    new_unit = {
                        "target": unit["target"][0],
                        "opinion": unit["opinion"][0],
                        "aspect": unit["aspect"],
                        "polarity": unit["polarity"],
                    }
                    new_data["comment_units"].append(new_unit)
                if (num_tgt_segs == 0) and (num_opn_segs == 1):
                    new_unit = {
                        "target": None,
                        "opinion": unit["opinion"][0],
                        "aspect": unit["aspect"],
                        "polarity": unit["polarity"],
                    }
                    new_data["comment_units"].append(new_unit)
                if (num_tgt_segs == 1) and (num_opn_segs == 0):
                    new_unit = {
                        "target": unit["target"][0],
                        "opinion": None,
                        "aspect": unit["aspect"],
                        "polarity": unit["polarity"],
                    }
                    new_data["comment_units"].append(new_unit)
            if len(new_data["comment_units"]) > 0:
                new_data_list.append(new_data)

    file_path = "/data1/chenfang/Project/JDComment/data/comment_filtered.json"
    with open(file_path, mode="w", encoding="utf-8") as file:
        for new_data in new_data_list:
            file.write(json.dumps(new_data, ensure_ascii=False) + "\n")


def split():
    # comment_filtered.json >> train.json, valid.json
    data_list = []
    file_path = "/data1/chenfang/Project/JDComment/data/comment_filtered.json"
    with open(file_path, mode="r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line.strip())
            data_list.append(data)

    random.seed(77)
    random.shuffle(data_list)
    num_train = int(len(data_list) * 0.9)
    train_data_list = sorted(data_list[:num_train], key=lambda x: x["comment_id"], reverse=False)
    valid_data_list = sorted(data_list[num_train:], key=lambda x: x["comment_id"], reverse=False)

    file_path = "/data1/chenfang/Project/JDComment/data/train.json"
    with open(file_path, mode="w", encoding="utf-8") as file:
        for new_data in train_data_list:
            file.write(json.dumps(new_data, ensure_ascii=False) + "\n")

    file_path = "/data1/chenfang/Project/JDComment/data/valid.json"
    with open(file_path, mode="w", encoding="utf-8") as file:
        for new_data in valid_data_list:
            file.write(json.dumps(new_data, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    reformat()
    filter()
    split()
