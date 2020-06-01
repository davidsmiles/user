import os

from dotenv import load_dotenv

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from db import db
from ma import ma

# Models
from models.profile import Profile

# Resources
from resources.profile import Profile
from resources.signup import UserSignUp
from resources.login import UserLogin
from resources.user import User
from resources.useridentity import UserIdentity
from resources.users import Users

app = Flask(__name__)

load_dotenv('.env')
app.config.from_object(os.environ['APPLICATION_SETTINGS'])

# in-app use
db.init_app(app)
ma.init_app(app)

api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_all():
    db.create_all()

    
# User
api.add_resource(User, '/users/<string:user_id>')
api.add_resource(Users, '/users')
api.add_resource(UserSignUp, '/users/signup')
api.add_resource(UserLogin, '/users/login')
api.add_resource(UserIdentity, '/users/identify/<string:user_id>')

# Profile
api.add_resource(Profile, '/users/<string:user_id>/profile')


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(host='0.0.0.0')
