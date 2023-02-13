import os
from lib.util.IO import update_doc, get_docs
import shutil
import json


class Collection:

    def __init__(self, instance):
        self.Instance = instance
        self.schema = None
        self.collectionName = None

    def create_collection(self, schema):
        self.verify_instance()

        collection_name = schema['collection_name']
        path = 'data/instances/' + self.Instance.credential_dict[
            'instance_name'] + '/' + collection_name

        try:

            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            update_doc(
                path + '/meta.json', {
                    "collection_name": collection_name,
                    "schema": schema['schema'],
                    "mapper": [{
                        "1.json": [0, 1000, False]
                    }]
                })

            self.schema = schema['schema']

            # get the collection data from instance meta
            data = get_docs('data/instances/' +
                            self.Instance.credential_dict['instance_name'] +
                            "/" +
                            self.Instance.credential_dict['instance_name'] +
                            ".json")

            for index, item in enumerate(data['collections']):
                if item['collection_name'] == collection_name:
                    raise Exception('Collection name is already taken!')

            data['collections'].append({
                "collection_name": collection_name,
                "schema": schema['schema']
            })

            update_doc(
                'data/instances/' +
                self.Instance.credential_dict['instance_name'] + "/" +
                collection_name + "/1.json", {})

            update_doc(
                'data/instances/' +
                self.Instance.credential_dict['instance_name'] + "/" +
                self.Instance.credential_dict['instance_name'] + ".json", data)

            return True

        except Exception as e:

            raise Exception('Error while creating new collection')

    def delete_collection(self, collection_name):
        collection_name = collection_name
        path = 'data/instances/' + self.Instance.credential_dict[
            'instance_name'] + '/' + collection_name

        try:

            shutil.rmtree(path)

            f = open('data/instances/' +
                     self.Instance.credential_dict['instance_name'] + '/' +
                     self.Instance.credential_dict['instance_name'] + '.json')
            meta_data = json.load(f)

            for index, item in enumerate(meta_data['collections']):
                if item['collection_name'] == collection_name:
                    del meta_data['collections'][index]

            update_doc(
                'data/instances/' +
                self.Instance.credential_dict['instance_name'] + '/' +
                self.Instance.credential_dict['instance_name'] + '.json',
                meta_data)

            return True

        except Exception as e:

            raise Exception("Error while deleting collection")

    def verify_instance(self):
        if not self.Instance.CONNECTION_ESTABLISHED:
            raise Exception('Connection failed')
