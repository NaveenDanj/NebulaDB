from flask_restful import Resource, request
from flask import g, jsonify
from marshmallow import Schema, fields
import uuid

from lib.core.Collection import Collection


class CollectionController(Resource):

    def post(self):

        data = request.json

        class Validator(Schema):
            collection_name = fields.Str(required=True)
            instance_name = fields.Str(required=True)
            secret = fields.Str(required=True)

        schema = Validator()
        errors = schema.validate(data)
        if errors:
            return {"message": errors}, 400

        collection = Collection(nebulaDBConnection)
        # collection.schema = {
        #     "id": "number",
        #     "username": "string",
        #     "password": "string",
        #     "wage": "number",
        #     "isMarried": "boolean",
        # }
        # collection.collectionName = 'user_collection'

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
