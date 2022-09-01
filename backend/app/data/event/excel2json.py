import json
import xlrd


def process_data(filepath):
    work_sheet = xlrd.open_workbook(filepath)
    work_table = work_sheet.sheets()[0]
    data_list = []
    for i in range(work_table.nrows):
        data_list.append({"text":work_table.cell_value(i,0), "id":i})

    to_file_path = "./changsha_data_unlabeled.json"
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