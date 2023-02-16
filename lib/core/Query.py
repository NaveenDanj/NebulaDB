import json


class Query:

    def __init__(self, instance):
        self.instance = instance
        self.collection = None
        self.data = None
        self.schema = None

    def collection(self, collection_name):
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
        return self

    def where(self, key, op, val):
        self.__validate_schema(key)

        if op not in ['==', '!=', '>', '<', '<=', '=>', 'like']:
            raise Exception('Invalid operator : ', op)

        if key == '==':
            self.__get_docs_by_where_condition_equals(key, val)
        elif key == '!=':
            self.__get_docs_by_where_condition_not_equals(key, val)
        elif key == '>':
            self.__get_docs_by_where_condition_grater_than(key, val)
        elif key == '<':
            self.__get_docs_by_where_condition_less_than(key, val)
        elif key == '<=':
            self.__get_docs_by_where_condition_less_than_equals(key, val)
        elif key == '=>':
            self.__get_docs_by_where_condition_grater_than_equals(key, val)
        elif key == 'like':
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
            filename = list(_file.keys())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)
            docs = docs + meta_data

        self.data = docs
        return self

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

        raise Exception('Document not Found!')

    def __validate_schema(self, key):
        if key not in self.schema:
            raise Exception('Schema validation error! key :', key,
                            " not found.")

        return True

    def __get_docs_by_where_condition_equals(self, key, val):

        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.keys())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            for item in meta_data:

                if item[key] == val:
                    docs.append(item)

        self.data = docs
        return self

    def __get_docs_by_where_condition_not_equals(self, key, val):

        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.keys())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            for item in meta_data:

                if item[key] != val:
                    docs.append(item)

        self.data = docs
        return self

    def __get_docs_by_where_condition_grater_than(self, key, val):

        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.keys())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            for item in meta_data:

                if item[key] > val:
                    docs.append(item)

        self.data = docs
        return self

    def __get_docs_by_where_condition_less_than(self, key, val):

        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.keys())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            for item in meta_data:

                if item[key] < val:
                    docs.append(item)

        self.data = docs
        return self

    def __get_docs_by_where_condition_grater_than_equals(self, key, val):

        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.keys())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            for item in meta_data:

                if item[key] >= val:
                    docs.append(item)

        self.data = docs
        return self

    def __get_docs_by_where_condition_less_than_equals(self, key, val):

        files = self.get_all_document_holders()

        docs = []

        for _file in files:
            filename = list(_file.keys())[0]

            f = open('data/instances/' +
                     self.instance.Instance.Instance['instance_name'] + '/' +
                     self.collection + '/' + filename)

            meta_data = json.load(f)

            for item in meta_data:

                if item[key] <= val:
                    docs.append(item)

        self.data = docs
        return self
