import json
import os

def get_docs(path):
    f = open(path)
    return json.load(f)


def update_doc(path, data):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)