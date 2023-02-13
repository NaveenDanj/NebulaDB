from flask_restful import Resource, request
from flask import g, jsonify
from marshmallow import Schema, fields
import uuid

from lib.core.Instance import Instance


def add_header(func):

    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.headers['X-Custom-Header'] = 'Value'

        data = request.headers

        class Validator(Schema):
            connection_id = fields.Str(required=True)
            instance_name = fields.Str(required=True)
            secret = fields.Str(required=True)

        schema = Validator()
        errors = schema.validate(data)
        if errors:
            return {"message": errors}, 400

        cursor = g.db.cursor()
        cursor.execute("SELECT * FROM connections WHERE connection_id = '" +
                       data['connection_id'] + "' ")
        connection = cursor.fetchall()
        g.db.close()

        if connection == []:
            return {
                "message":
                "Invalid connection credentials. No valid connection found!"
            }, 404

        conn = connection[0]

        if not data['instance_name'] == conn[1]:
            return {
                "message": "Invalid connection credentials. Invalid instance!"
            }, 400

        if not data['secret'] == conn[2]:
            return {"message": "Invalid connection credentials"}, 400

        return func(*args, **kwargs)

    return wrapper