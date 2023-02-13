from flask_restful import Resource
from lib.core.Connection import Connection
from lib.core.Collection import Collection
from lib.core.Document import Document


class TestController(Resource):

    def get(self):

        nebulaDBConnection = Connection({
            "connection_id":
            "e291770d77a54fe8b330a0c5807662f5",
            "instance_name":
            "default_instance_4",
            "secret":
            "3cbc3a7f5ffc4acf8da39f21c40c91d2"
        })
        nebulaDBConnection.connect()

        collection = Collection(nebulaDBConnection)
        collection.schema = {
            "id": "number",
            "username": "string",
            "password": "string",
            "wage": "number",
            "isMarried": "boolean",
        }
        collection.collectionName = 'user_collection'

        # collection.create_collection({
        #     "collection_name": "user_collection",
        #     "schema": {
        #         "id": "number",
        #         "username": "string",
        #         "password": "string",
        #         "wage": "number",
        #         "isMarried": "boolean",
        #     }
        # })

        doc = Document(
            collection, {
                "id": 123,
                "username": "naveendan",
                "password": "naveendan830",
                "wage": 12000.00,
                "isMarried": False,
            }, nebulaDBConnection)

        ret = doc.create()

        return ret

        # collection.delete_collection('user_collection')

        return {
            "message": nebulaDBConnection.get_connection_status(),
        }, 200
