from flask_restful import Resource, request
from flask import g, jsonify
from marshmallow import Schema, fields
import uuid
from lib.core.Instance import Instance


def EnsureConnection(func):

    def wrapper(*args, **kwargs):
        data = request.headers

        if 'connection_id' not in data or 'instance_name' not in data or 'secret' not in data:
            return {'messages': 'Invalid connection credentials'}, 400

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