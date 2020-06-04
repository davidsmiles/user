import os

from dotenv import load_dotenv

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from extensions import *
from resources.routes import initialize_routes

app = Flask(__name__)

load_dotenv('.env')
app.config.from_object(os.environ['APPLICATION_SETTINGS'])

api = Api(app)
jwt = JWTManager(app)


if __name__ == '__main__':
    initialize_extensions(app)
    initialize_routes(api)
    app.run(host='0.0.0.0')
