import json


def load_json(file):
    with open(file, 'r', encoding='utf8') as f:
        data = json.load(f)
    return data


def save_json(data, file):
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def default_load_json(json_file, encoding='utf-8', **kwargs):
    with open(json_file, 'r', encoding=encoding) as fin:
        data = json.load(fin, **kwargs)
        return data


def default_dump_json(obj, json_file, encoding='utf-8', ensure_ascii=False, indent=2, **kwargs):
    with open(json_file, 'w', encoding=encoding) as fout:
        json.dump(obj, fout, ensure_ascii=ensure_ascii,
                  indent=indent, **kwargs)


