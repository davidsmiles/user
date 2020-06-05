from flask import request, Response, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from mongoengine.errors import DoesNotExist, InvalidQueryError

from database.models import Users
from libs.errors import *
from libs.strings import gettext


class Address(Resource):
    
    @classmethod
    @jwt_required
    def get(cls):
        _id = get_jwt_identity()

        try:
            address = Users.objects.get(id=_id).address
        except DoesNotExist:
            return {
                   'message': gettext('user_not_found'),
                   'code': 404
            }, 404

        return jsonify(address)

    @classmethod
    @jwt_required
    def post(cls):
        _id = get_jwt_identity()

        data = request.get_json()
        try:
            user = Users.objects.get(id=_id)
            user.update(push__address=data.get('address'))
            user.save()
        except DoesNotExist:
            raise UserNotExist
        except InvalidQueryError:
            raise QueryInvalidError
        return {}, 200

    @classmethod
    def put(cls, id):
        pass

    @classmethod
    def delete(cls, id):
        pass
