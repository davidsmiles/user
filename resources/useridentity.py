from flask_restful import Resource

from libs.strings import gettext
from models.usermodel import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class UserIdentity(Resource):
    @classmethod
    def get(cls, user_id):
        """
        This Resource is only requested from other Services
        :param user_id: of a User in the DB
        :return: if valid, returns User's ID
        """
        user = UserModel.find_by_userid(user_id)
        if not user:
            return {'message': gettext('user_not_found'), 'code': 404}, 404

        return {'id': user.id}, 200
