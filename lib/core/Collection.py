import os
from lib.util.IO import update_doc, get_docs


class Collection:

    def __init__(self, instance):
        self.Instance = instance

    def create_collection(self, schema):
        self.verify_instance()

        collection_name = schema['collection_name']
        path = 'data/instances/' + self.Instance.credential_dict[
            'instance_name'] + '/' + collection_name

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        update_doc(path + '/meta.json', {
            "collection_name": collection_name,
            "schema": schema['schema']
        })

        # get the collection data from instance meta
        data = get_docs('data/instances/' +
                        self.Instance.credential_dict['instance_name'] + "/" +
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
            self.Instance.credential_dict['instance_name'] + ".json", data)

    def verify_instance(self):
        if not self.Instance.CONNECTION_ESTABLISHED:
            raise Exception('Connection failed')
