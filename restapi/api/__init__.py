from flask import Flask, request
from flask_restful import Api, reqparse
from flask_apispec import FlaskApiSpec
from pymongo import MongoClient
from .models import User, instance
from .controllers import UserController, UsersController

MODELS = [User]

def init_api(app):
    api = Api(app)
    for model in MODELS:
        model.ensure_indexes()
    api.add_resource(UsersController, '/users')
    api.add_resource(UserController, '/users/<user_id>')
    return api

def init_swagger(app):
    docs = FlaskApiSpec(app)
    docs.register(UsersController)
    docs.register(UserController)
    return docs

def create_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('dbid', help='The name of the database we wish to add to')
    return parser

con = MongoClient('mongo:27017')
parser = create_parser()

def initiate_db_connection():
    if request:
        if dbid := parser.parse_args()['dbid'] is not None:
            instance.init(con[dbid])
    else:
        instance.init(con['app'])

def create_app(config_filename='config.py'):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    initiate_db_connection()
    app.before_request(initiate_db_connection)

    # Initialize API and Swagger
    init_api(app)
    init_swagger(app)

    return app
