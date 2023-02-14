from flask import Flask
from flask_restful import Api
from server.controllers.Connection import ConnectionController, CrudConnectionController
from server.controllers.Collection import CollectionController
from server.controllers.Test import TestController
import sqlite3
from flask import g

app = Flask(__name__)
api = Api(app)


@app.before_request
def before_request():
    g.db = sqlite3.connect("database.db")
    g.db.execute("""
        CREATE TABLE IF NOT EXISTS `connections` (
            `connection_id` VARCHAR(512) NOT NULL UNIQUE PRIMARY KEY,
            `instance_name` VARCHAR(100) NOT NULL,
            `secret` VARCHAR(512) NOT NULL
        );
    """)


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():

    return {
        "message":
        "Welcome to NebulaDB",
        "server-info":
        'Welcome to NebulaDB!\nServer information:\n{}'.format(app.config)
    }, 200


api.add_resource(ConnectionController, '/api/connection')
api.add_resource(CrudConnectionController, '/api/crud-connection')
api.add_resource(CollectionController, '/api/crud-collection')
api.add_resource(TestController, '/api/test')

if __name__ == "__main__":
    app.run(debug=True, port=8300)
