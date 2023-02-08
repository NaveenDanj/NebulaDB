from flask_restful import Resource, request
from flask import g, jsonify


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
        return {"response": "OK", "data": data}, 200
