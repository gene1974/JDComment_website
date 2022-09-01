import json
import re


def process_data(filepath):
    from_file = open(filepath, "r", encoding="utf-8")
    data_list = []
    for line in from_file:
        data_list.append(json.loads(line.strip()))
    from_file.close()

    to_file_path = "./nongchanpin.json"
    to_file =  open(to_file_path, "w", encoding="utf-8")
    to_file.write(json.dumps(data_list, ensure_ascii=False, indent=2))
    to_file.close()

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=str)
    args = parser.parse_args()
    print('start data processing %s'%args.filepath)
    process_data(args.filepath)