import json
from .filesystem import check_file


def read_json(path: str):
    check_file(path)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path: str, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
