from flask import request, Response
from flask_restful import Resource

from mongoengine.errors import DoesNotExist, InvalidQueryError

from database.models import Users
from libs.strings import gettext


class User(Resource):
    
    @classmethod
    def get(cls, id):
        try:
            user = Users.objects.get(id=id)
        except DoesNotExist:
            return {
                   'message': gettext('user_not_found'),
                   'code': 404
            }, 404
        return Response(user.to_json(), mimetype="application/json", status=200)

    @classmethod
    def put(cls, id):
        data = request.get_json()
        try:
            user = Users.objects.get(id=id)
            user.update(**data)
        except DoesNotExist:
            return {
                   'message': gettext('user_not_found'),
                   'code': 404
            }, 404
        except InvalidQueryError:
            return {
                   'message': gettext('unexpected_user_data'),
                   'code': 400
            }, 400
        return "OK", 200

    @classmethod
    def delete(cls, id):
        user = request.get_json()
        try:
            user = Users.objects.get(id=id)
            user.delete()
        except DoesNotExist:
            return {
                'message': gettext('user_not_found'),
                'code': 404
            }, 404

        return {}, 204
