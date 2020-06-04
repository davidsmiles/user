import datetime

from flask import request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource

from mongoengine.errors import DoesNotExist

from database.models import Users
from libs.strings import gettext


class AccountLogin(Resource):

    @classmethod
    def post(cls):
        data = request.get_json()
        try:
            user =  Users.objects.get(email=data.get('email'))
            authorized = user.check_password(data.get('password'))

            if not authorized:
                return {
                    'message': gettext("user_invalid_credentials"),
                    'status': 401
               }, 401
            
            expires = datetime.timedelta(days=7)  # 7 Day
            access_token = create_access_token(
                identity=str(user.id),
                fresh=True,
                expires_delta=expires)
            refresh_token = create_refresh_token(identity=str(user.id))

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        except DoesNotExist:
            return {
                   'message': gettext('user_not_found'),
                   'status': 404
               }, 404
