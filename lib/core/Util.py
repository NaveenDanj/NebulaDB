from lib.util.IO import get_docs


class Util:

    def __init__(self, instance):
        self.instance = instance

    def get_all_collections(self):

        path = 'data/instances/' + self.instance.credential_dict[
            'instance_name'] + '/' + self.instance.credential_dict[
                'instance_name'] + ".json"

        data = get_docs(path)
        return data['collections']

    def verify_instance(self):
        if not self.Instance.CONNECTION_ESTABLISHED:
            raise Exception('Connection failed')
