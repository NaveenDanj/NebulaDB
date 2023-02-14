from flask_restful import Resource, request
from flask import g, jsonify
from marshmallow import Schema, fields
import uuid

from lib.core.Collection import Collection
from lib.core.Connection import Connection
from server.middleware.EnsureConnection import EnsureConnection


class CollectionController(Resource):

    @EnsureConnection
    def post(self):

        data = request.json

        class Validator(Schema):
            collection_name = fields.Str(required=True)
            schema = fields.Dict(required=True)

        schema = Validator()
        errors = schema.validate(data)
        if errors:
            return {"message": errors}, 400

        try:
            headers = request.headers

            nebulaDBConnection = Connection({
                "connection_id":
                headers["connection_id"],
                "instance_name":
                headers["instance_name"],
                "secret":
                headers["secret"]
            })
            nebulaDBConnection.connect()
            collection = Collection(nebulaDBConnection)

            collection.create_collection({
                "collection_name":
                data['collection_name'],
                "schema":
                data['schema']
            })

            return {
                "message": "New collection created!",
                "collection": data['schema']
            }, 200

        except Exception as e:
            return {
                "message": "Error while creating a collection",
            }, 400

    @EnsureConnection
    def delete(self):

        data = request.json

        class Validator(Schema):
            collection_name = fields.Str(required=True)

        schema = Validator()
        errors = schema.validate(data)
        if errors:
            return {"message": errors}, 400

        # check collection exists!
        try:
            headers = request.headers

            nebulaDBConnection = Connection({
                "connection_id":
                headers["connection_id"],
                "instance_name":
                headers["instance_name"],
                "secret":
                headers["secret"]
            })
            nebulaDBConnection.connect()
            collection = Collection(nebulaDBConnection)

            collection.delete_collection(data['collection_name'])

            return {
                "message": "Collection deleted successfully",
            }, 200

        except Exception as e:
            return {
                "message": "Error while creating a collection",
            }, 400
