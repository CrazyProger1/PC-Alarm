import json
from .filesystem import check_file


def read_json(path: str):
    check_file(path)
    with open(path, 'r') as f:
        return json.load(f)


def write_json(path: str, data):
    with open(path, 'w') as f:
        json.dump(data, f)
