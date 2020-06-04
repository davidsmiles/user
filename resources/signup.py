from flask import request
from flask_restful import Resource

from database.models import Users
from libs.strings import gettext
from mongoengine.errors import NotUniqueError


class AccountSignUp(Resource):
    @classmethod
    def post(cls):
        # Get the Json payload
        data = request.get_json()
        # Load it into a User object
        user = Users(**data)

        try:
            user.hash_password()
            user.save()
            _id = user.id
            
            return {'id': str(_id)}, 200
        except NotUniqueError:
            return {
                'message': gettext("user_username_exists"),
                'code': 400
            }, 400