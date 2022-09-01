# -*- coding: utf-8 -*-

from code.config import get_default_args
from code.factory import Factory


# export PYTHONPATH=$PYTHONPATH:/data1/chenfang/Project/JDComment
# CUDA_VISIBLE_DEVICES=1 python3 example.py


def main():
    # 配置模型
    root = "."  # 项目根目录
    args = get_default_args(root=root)  # 默认参数
    factory = Factory(args)
    factory.initialize()  # 初始化

    # 输入格式
    # data_list: [
    #     {"comment_text": "xxx"}
    # ]
    data_list = []
    data_list.append({"comment_text": "花生品质及物流，都不错，如果邮寄前把个别憋的检出来，就完美了。"})
    data_list.append({"comment_text": "质量很好，纯棉的没有线头，干净利落好看颜色。"})
    data_list.append({"comment_text": "很好，价格也不贵，再大点就好了。"})
    data_list.append({"comment_text": "包装不好，有点脏，里面比较湿，有两个是坏的。"})
    data_list.append({"comment_text": "大米都生虫了，而且大米颜色也有点暗，不新鲜。"})
    data_list.append({"comment_text": "物流配送快，份量够，个头挺大的。"})

    # 调用模型
    results = factory.infer(data_list)

    # 输出格式
    # results: [
    #     {"comment_units": [(tgt_head, tgt_tail, opn_head, opn_tail, category, polarity)]}
    # ]
    for i in range(len(data_list)):
        print("-----------------------------------------------------")
        comment_text = data_list[i]["comment_text"]
        comment_units = results[i]["comment_units"]
        print(comment_text)
        for tgt_head, tgt_tail, opn_head, opn_tail, category, polarity in comment_units:
            if (tgt_head is not None) and (tgt_tail is not None):
                tgt_text = comment_text[tgt_head:tgt_tail]
            else:
                tgt_text = None
            if (opn_head is not None) and (opn_tail is not None):
                opn_text = comment_text[opn_head:opn_tail]
            else:
                opn_text = None
            print("{}({}, {}) - {}({}, {}) - {} - {}".format(tgt_text, tgt_head, tgt_tail, opn_text, opn_head, opn_tail, category, polarity))
    return None


if __name__ == "__main__":
    main()
