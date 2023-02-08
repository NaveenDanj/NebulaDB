from flask import Flask
from flask_restful import Api
from server.controllers.Connection import ConnectionController
import sqlite3
from flask import g
from lib.util.Password import hash_password

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

    g.db.execute("""
        INSERT INTO connections(connection_id , username , password , instance_name)
        VALUES('001' , 'admin' , '""" + hash_password('admin123') +
                 """' , 'default_instance')
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

if __name__ == "__main__":
    app.run(debug=True, port=8300)
