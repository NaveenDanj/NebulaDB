import uuid
from lib.util.IO import update_doc, get_docs
import json


class Document:

    def __init__(self, collection, DocumentSchema, Instance):
        self.documentSchema = DocumentSchema
        self.instance = Instance
        self.collection = collection
        self._id = None

    def create(self):
        self.verifySchema()
        self._id = uuid.uuid4().hex

        # choose document holder
        doc_holder = self.choose_document_holder()

        path = 'data/instances/' + self.instance.Instance.Instance[
            'instance_name'] + '/' + self.collection.collectionName + "/" + doc_holder[
                'filename']
        self.documentSchema['_id'] = self._id

        f = open(path)
        meta_data = json.load(f)
        meta_data[self._id] = self.documentSchema

        update_doc(path, meta_data)

        return self.documentSchema

    def verifySchema(self):

        keys = []

        for key in self.collection.schema:
            keys.append(key)

        for key in self.documentSchema:
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
