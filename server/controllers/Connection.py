from flask_restful import Resource
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
        return {"response": "OK"}, 200
