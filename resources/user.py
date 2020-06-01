from flask import request
from flask_restful import Resource

from libs.strings import gettext
from models.usermodel import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {
                   'message': gettext('user_not_found'),
                   'code': 404
            }, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {
                'message': gettext('user_not_found'),
                'code': 404
            }, 404

        user.delete_from_db()
        return {}, 204
