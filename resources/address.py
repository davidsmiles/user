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
            address = Users.objects(id=_id).only('address').first().address
        except DoesNotExist:
            raise UserNotExist

        return jsonify(address)

    @classmethod
    @jwt_required
    def post(cls):
        _id = get_jwt_identity()

        data = request.get_json()
        try:
            user = Users.objects(id=_id)
            user.update(push__address=data)
        except DoesNotExist:
            raise UserNotExist
        except InvalidQueryError:
            raise QueryInvalidError
        return {}, 200

    @classmethod
    @jwt_required
    def put(cls):
        _id = get_jwt_identity()

        position = request.args['position']
        data = request.get_json()

        from database.models import Address
        address = Address(**data)

        try:
            user = Users.objects(id=_id)

            count = len(user.first().address)

            if int(position) >= count or int(position) <= 0:
                return {
                    "message": gettext('out_of_list_index'),
                    "status": 400
                }

            user.update_one(**{f'set__address__{position}': address})
        except DoesNotExist:
            raise UserNotExist
        except InvalidQueryError:
            raise InvalidQueryError
        return {}, 200


    @classmethod
    def delete(cls):
        pass
