import os

from dotenv import load_dotenv

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from extensions import *

# Resources
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.signup import AccountSignUp
from resources.login import AccountLogin
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
api.add_resource(UserIdentity, '/users/identify/<string:user_id>')

# Account
api.add_resource(AccountSignUp, '/accounts/signup')
api.add_resource(AccountLogin, '/accounts/login')
api.add_resource(Confirmation, '/accounts/confirmation/<string:confirmation_id>')
api.add_resource(ConfirmationByUser, '/accounts/confirmation/user/<string:user_id>')


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(host='0.0.0.0')
