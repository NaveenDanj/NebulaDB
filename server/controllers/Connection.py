from flask_restful import Resource, request
from flask import g, jsonify
from marshmallow import Schema, fields
from lib.util.Password import check_password
from lib.util.JWTHelper import encode_auth_token


class ConnectionController(Resource):

    def get(self):
        cursor = g.db.cursor()
        cursor.execute(
            "SELECT connection_id , username , instance_name FROM connections")
        connection = cursor.fetchall()
        g.db.close()
        return jsonify(connection)

    def post(self):

        data = request.json

        class Validator(Schema):
            username = fields.Str(required=True)
            password = fields.Str(required=True)
            connection_id = fields.Str(required=True)
            instance_id = fields.Str(required=True)

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

        if not data['username'] == conn[1]:
            return {
                "message":
                "Invalid connection credentials. Username or password incorrect!"
            }, 400

        if not check_password(data['password'], conn[2]):
            return {
                "message":
                "Invalid connection credentials. Username or password incorrect!"
            }, 400

        if not data['instance_id'] == conn[3]:
            return {
                "message": "Invalid connection credentials. Invalid instance!"
            }, 400

        # genarate jwt token
        token = encode_auth_token(data['connection_id'])
        return {"connection": conn, "token": token}, 200
