from flask_restful import Resource, request
from flask import g, jsonify
from marshmallow import Schema, fields
from lib.core.Connection import Connection
from lib.core.Collection import Collection


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
        collection.create_collection({
            "collection_name": "new_collection",
            "schema": {
                "id": "number",
                "username": "string",
                "password": "string",
                "wage": "number",
                "isMarried": "boolean",
            }
        })

        return {
            "message": nebulaDBConnection.get_connection_status(),
        }, 200
