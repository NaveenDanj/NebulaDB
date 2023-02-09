from flask_restful import Resource, request
from flask import g, jsonify
from marshmallow import Schema, fields
import uuid


class ConnectionController(Resource):

    def get(self):
        cursor = g.db.cursor()
        cursor.execute("SELECT * FROM connections")
        connection = cursor.fetchall()
        g.db.close()
        return jsonify(connection)

    def post(self):

        data = request.json

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

        return {"connection": conn}, 200


class CrudConnectionController(Resource):

    def post(self):

        data = request.json

        class Validator(Schema):
            instance_name = fields.Str(required=True)

        schema = Validator()
        errors = schema.validate(data)
        if errors:
            return {"message": errors}, 400

        conn = g.db.execute(
            "SELECT * FROM connections WHERE instance_name = '" +
            data['instance_name'] + "' LIMIT 1")
        conn = conn.fetchall()

        if conn != []:
            return {"message": "Instance name already taken"}, 400

        secret = uuid.uuid4().hex
        connection_id = uuid.uuid4().hex

        g.db.execute("""
            INSERT INTO connections(connection_id , instance_name , secret)
            VALUES('""" + connection_id + """' , '""" + data['instance_name'] +
                     """' , '""" + secret + """')
        """)

        g.db.commit()

        g.db.close()
        # create new instance from core

        return {
            "message": "New instance created!",
        }, 200

    def delete(self):

        data = request.json

        class Validator(Schema):
            instance_name = fields.Str(required=True)

        schema = Validator()
        errors = schema.validate(data)
        if errors:
            return {"message": errors}, 400

        connection = g.db.execute(
            "SELECT * FROM connections WHERE instance_name = '" +
            data['instance_name'] + "' LIMIT 1")
        connection = connection.fetchall()

        if connection == []:
            return {"message": "No valid connection found!"}, 404

        g.db.execute("DELETE FROM connections WHERE instance_name = '" +
                     data['instance_name'] + "'")
        g.db.commit()
        g.db.close()

        # delete instance from core

        return {"message": "Instance deleted successfully!"}, 200
