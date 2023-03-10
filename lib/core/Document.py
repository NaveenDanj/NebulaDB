import uuid
from lib.util.IO import update_doc, get_docs
import json


class Document:

    def __init__(self, collection, DocumentSchema, Instance):
        self.data = DocumentSchema
        self.instance = Instance
        self.collection = collection
        self._id = None
        self.filepath = None

    def create(self):
        self.verifySchema()
        self._id = uuid.uuid4().hex

        # choose document holder
        doc_holder = self.choose_document_holder()

        path = 'data/instances/' + self.instance.Instance.Instance[
            'instance_name'] + '/' + self.collection.collectionName + "/" + doc_holder[
                'filename']
        self.data['_id'] = self._id

        f = open(path)
        meta_data = json.load(f)
        meta_data[self._id] = self.data

        update_doc(path, meta_data)
        self.filepath = path
        return self.data

    def delete(self):
        data = self.check_document_exists(self._id)

        if data == False:
            raise Exception("Document not found!")

        f = open(data['filepath'])
        meta_data = json.load(f)

        del meta_data[self._id]

        update_doc(data['filepath'], meta_data)

        return True

    def verifySchema(self):

        keys = []

        for key in self.collection.schema:
            keys.append(key)

        for key in self.data:
            if key not in keys:
                raise Exception("Missing key : ", key)

        return True

    def choose_document_holder(self):
        f = open('data/instances/' +
                 self.instance.Instance.Instance['instance_name'] + '/' +
                 self.collection.collectionName + '/meta.json')
        meta_data = json.load(f)

        for item in meta_data['mapper']:
            filename = list(item.keys())[0]
            if item[filename][2] == False:
                return {
                    "filename": filename,
                    "data": item[filename],
                }

        raise Exception('Document limit reached!')

    def check_document_exists(self, _id):

        f = open('data/instances/' +
                 self.instance.Instance.Instance['instance_name'] + '/' +
                 self.collection.collectionName + '/meta.json')
        meta_data = json.load(f)

        for item in meta_data['mapper']:
            filename = list(item.keys())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection.collectionName + '/' + filename)

            meta_data = json.load(f)

            if _id in meta_data:
                return {
                    "filepath":
                    'data/instances/' +
                    self.instance.Instance.Instance['instance_name'] + '/' +
                    self.collection.collectionName + '/' + filename,
                    "data":
                    meta_data[_id],
                }

        return False