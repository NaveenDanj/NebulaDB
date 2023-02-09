from flask_restful import Resource, request
from flask import g, jsonify
from marshmallow import Schema, fields
from lib.core.Connection import Connection


class TestController(Resource):

    def get(self):

        nebulaDBConnection = Connection({
            "connection_id":
            "bffd5abbb5804734bee56b4b56b21c59",
            "instance_name":
            "default_instance",
            "secret":
            "6d62d65af77b4ba993642b5d13bbab88"
        })

        nebulaDBConnection.connect()

        return {
            "message": nebulaDBConnection.get_connection_status(),
        }, 200
