from flask_restful import Resource

from models.usermodel import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class Users(Resource):
    @classmethod
    def get(cls):
        return user_schema.dump(UserModel.find_all(), many=True)
