from flask import Response
from flask_restful import Resource

from database.models import Users


class AllUsers(Resource):
    @classmethod
    def get(cls):
        users = Users.objects().to_json()
        return Response(users, content_type='application/json', status=200)