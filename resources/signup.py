import traceback

from flask import request
from flask_restful import Resource
from marshmallow import INCLUDE
from werkzeug.security import generate_password_hash

from libs.strings import gettext
from models.profile import Profile
from models.usermodel import UserModel
from schemas.user import UserSchema

user_schema = UserSchema(unknown=INCLUDE)


class UserSignUp(Resource):
    @classmethod
    def post(cls):
        # Get the Json payload
        data = request.get_json()
        # Load it into a User object
        user = user_schema.load(data)

        if UserModel.find_by_email(user.email):
            return {'message': gettext("user_username_exists")}, 302

        try:
            user.password = generate_password_hash(user.password)
            user.save_to_db()

            # Create a User Profile
            del(data['email'])
            del(data['password'])

            profile = Profile(**data)
            user.profile = profile

            profile.save_to_db()
            return user_schema.dump(user), 200
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {
                       'message': gettext("user_error_creating"),
                       'code': 500
                   }, 500
