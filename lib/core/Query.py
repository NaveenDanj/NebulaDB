import json
from lib.util.IO import update_doc


class Query:

    def __init__(self, instance):
        self.instance = instance
        self.collection = None
        self.data = None
        self.schema = None

    def set_collection(self, collection_name):
        self.collection = collection_name

        f = open('data/instances/' +
                 self.instance.Instance.Instance['instance_name'] + '/' +
                 self.collection + '/meta.json')

        meta_data = json.load(f)
        self.schema = meta_data['schema']

        return self

    def get_doc_by_id(self, _id):
        data = self.check_document_exists(_id)
        self.data = data['data']

    def where(self, key, op, val):
        self.__validate_schema(key)

        if op not in ['==', '!=', '>', '<', '<=', '=>', 'like']:
            raise Exception('Invalid operator : ', op)

        if op == '==':
            self.__get_docs_by_where_condition_equals(key, val)
        elif op == '!=':
            self.__get_docs_by_where_condition_not_equals(key, val)
        elif op == '>':
            self.__get_docs_by_where_condition_grater_than(key, val)
        elif op == '<':
            self.__get_docs_by_where_condition_less_than(key, val)
        elif op == '<=':
            self.__get_docs_by_where_condition_less_than_equals(key, val)
        elif op == '=>':
            self.__get_docs_by_where_condition_grater_than_equals(key, val)
        elif op == 'like':
            pass

        return self

    def first(self):
        self.data = self.data[0]
        return self

    def last(self):
        self.data = self.data[-1]
        return self

    def get_all_docs(self):

        if self.collection == None:
            raise Exception('Collection not found!')

        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.values())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)
            docs = docs + list(meta_data.values())

        self.data = docs
        return self

    def delete(self):

        for item in self.data:
            data = self.check_document_exists(item['_id'])

            if data == False:
                raise Exception("Document not found!")

            f = open(data['filepath'])
            meta_data = json.load(f)

            del meta_data[item['_id']]

            update_doc(data['filepath'], meta_data)

        return True

    def get_all_document_holders(self):

        try:
            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/meta.json')
            meta_data = json.load(f)

            files = []

            for item in meta_data['mapper']:
                filename = list(item.keys())[0]
                files.append({
                    "filename": filename,
                    "data": item[filename],
                })

            return files

        except Exception as e:
            raise Exception('No such a collection : ', self.collection)

    def choose_document_holder(self):
        try:

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/meta.json')
            meta_data = json.load(f)

            for item in meta_data['mapper']:
                filename = list(item.keys())[0]
                if item[filename][2] == False:
                    return {
                        "filename": filename,
                        "data": item[filename],
                    }

            raise Exception('Document limit reached!')
        except Exception as e:
            raise Exception('Error while finding documents!')

    def check_document_exists(self, _id):

        f = open('data/instances/' +
                 self.instance.Instance.Instance['instance_name'] + '/' +
                 self.collection + '/meta.json')
        meta_data = json.load(f)

        for item in meta_data['mapper']:
            filename = list(item.keys())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            if _id in meta_data:
                return {
                    "filepath":
                    'data/instances/' +
                    self.instance.Instance.Instance['instance_name'] + '/' +
                    self.collection + '/' + filename,
                    "data":
                    meta_data[_id],
                }

        raise Exception('Document not Found!')

    def __validate_schema(self, key):
        if key not in self.schema:
            raise Exception('Schema validation error! key :', key,
                            " not found.")

    def __get_docs_by_where_condition_equals(self, key, val):
        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.values())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            for item in meta_data:
                if meta_data[item][key] == val:
                    docs.append(meta_data[item])

        self.data = docs
        return self

    def __get_docs_by_where_condition_not_equals(self, key, val):

        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.values())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            for item in meta_data:

                if meta_data[item][key] != val:
                    docs.append(item)

        self.data = docs
        return self

    def __get_docs_by_where_condition_grater_than(self, key, val):

        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.values())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            for item in meta_data:

                if meta_data[item][key] > val:
                    docs.append(item)

        self.data = docs
        return self

    def __get_docs_by_where_condition_less_than(self, key, val):

        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.values())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            for item in meta_data:

                if meta_data[item][key] < val:
                    docs.append(item)

        self.data = docs
        return self

    def __get_docs_by_where_condition_grater_than_equals(self, key, val):

        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.values())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            for item in meta_data:

                if meta_data[item][key] >= val:
                    docs.append(item)

        self.data = docs
        return self

    def __get_docs_by_where_condition_less_than_equals(self, key, val):

        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.values())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            for item in meta_data:

                if meta_data[item][key] <= val:
                    docs.append(item)

        self.data = docs
        return self
