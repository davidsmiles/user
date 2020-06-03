import datetime

from flask import request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource
from marshmallow import EXCLUDE

from libs.strings import gettext
from models.usermodel import UserModel
from schemas.user import UserSchema

user_schema = UserSchema(unknown=EXCLUDE)


class AccountLogin(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        user = user_schema.load(data, partial=('email', 'password'))

        user = UserModel.find_by_email(user.email)
        if not user:
            return {
                   'message': gettext('user_not_found'),
                   'code': 404
               }, 404

        if UserModel.is_login_valid(user, data['password']):
            confirmation = user.most_recent_confirmation

            config = current_app.config

            if (confirmation and confirmation.confirmed) or config['TESTING']:
                expires = datetime.timedelta(seconds=84000)  # 1 Day
                access_token = create_access_token(
                    identity=user.user_id,
                    fresh=True,
                    expires_delta=expires)
                refresh_token = create_refresh_token(identity=user.user_id)

                return {
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }, 200
            return {"message": gettext("user_not_confirmed")}, 400
            
        return {
               'message': gettext("user_invalid_credentials"),
               'code': 401
               }, 401
