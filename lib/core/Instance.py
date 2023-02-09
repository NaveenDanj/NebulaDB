import json
import os
import shutil


class Instance:

    def __init__(self, instance_dict):
        self.Instance = instance_dict

    def get_instance(self):
        return self.Instance

    def create_instance(self, instance_dict):
        instance_name = instance_dict["instance_name"]
        path = 'data/instances/' + instance_name + '/' + instance_name + '.json'

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, 'w', encoding='utf-8') as f:
            data = {"instance_data": instance_dict, "collections": []}
            json.dump(data, f, ensure_ascii=False, indent=4)

        f = open('data/meta.json')
        meta_data = json.load(f)

        meta_data['instances'].append(instance_dict)

        with open('data/meta.json', 'w', encoding='utf-8') as f:
            data = {"instance_data": instance_dict, "collections": []}
            json.dump(meta_data, f, ensure_ascii=False, indent=4)

        return path

    def delete_instance(self, instance_dict):
        instance_name = instance_dict["instance_name"]
        path = 'data/instances/' + instance_name

        shutil.rmtree(path)

        f = open('data/meta.json')
        meta_data = json.load(f)

        for index, item in enumerate(meta_data['instances']):
            if item['instance_name'] == instance_dict["instance_name"]:
                del meta_data['instances'][index]

        with open('data/meta.json', 'w', encoding='utf-8') as f:
            json.dump(meta_data, f, ensure_ascii=False, indent=4)

        return path