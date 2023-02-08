from flask import Flask, request
from flask_restful import Api, Resource
from server.controllers.Connection import ConnectionController
import sqlite3
from flask import g

app = Flask(__name__)
api = Api(app)


@app.before_request
def before_request():
    g.db = sqlite3.connect("database.db")
    g.db.execute("""
        CREATE TABLE IF NOT EXISTS `connections` (
            `connection_id` VARCHAR(512) NOT NULL UNIQUE,
            `username` VARCHAR(255) NOT NULL UNIQUE,
            `password` VARCHAR(1024) NOT NULL,
            `instance_name` VARCHAR(100) NOT NULL
        );
    """)


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def hello_world():

    return {
        "message":
        "Welcome to NebulaDB",
        "server-info":
        'Welcome to my database server!\nServer information:\n{}'.format(
            app.config)
    }, 200


api.add_resource(ConnectionController, '/api/connection')

if __name__ == "__main__":
    app.run(debug=True, port=8300)
