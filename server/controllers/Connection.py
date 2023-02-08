from flask_restful import Api, Resource


class ConnectionController(Resource):

    def get(self):
        return {"response": "OK"}, 200

    def post(self):
        return {"response": "OK"}, 200
