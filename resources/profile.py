from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from libs.strings import gettext
from models.profile import Profile
from models.usermodel import UserModel
from schemas.user import UserSchema
from schemas.profile import ProfileSchema

user_schema = UserSchema()
profile_schema = ProfileSchema()


class Profile(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {
                "message": gettext("user_not_found"),
                "code": 404    
            }, 404

        return dict(profile_schema.dump(user.profile), **user_schema.dump(user)), 200
    
    @classmethod
    def put(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {
                   'message': gettext('user_not_found'),
                   'code': 404
               }, 404

        user.profile.update(request.get_json())
        return profile_schema.dump(user.profile), 200
