import traceback

from datetime import datetime
from time import time

from flask import render_template, make_response
from flask_restful import Resource

from libs.strings import gettext
from models.confirmation import ConfirmationModel
from models.usermodel import UserModel
from schemas.confirmation import ConfirmationSchema


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        """Return confirmation HTML page"""
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": gettext("confirmation_not_found")}, 404

        if confirmation.expired:
            return {"message": gettext("confirmation_link_expired")}, 400

        if confirmation.confirmed:
            return {"message": gettext("confirmation_already_confirmed")}, 400

        confirmation.confirmed = True
        confirmation.user.confirmed_at = datetime.utcnow()
        confirmation.save_to_db()

        headers = {"Content-Type": "text/html"}
        # return make_response(
        #     render_template("confirmation_page.html", email=confirmation.user.email),
        #     200,
        #     headers
        # )

        return {'message': gettext("user_confirmed")}, 200


confirmation_schema = ConfirmationSchema(many=True)


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        """Return confirmations for a giving user. Use for testing"""
        user = UserModel.find_by_id(user_id)

        if not user:
            return {"message": gettext('user_not_found')}, 404

        return {
            "current_time": int(time()),
            "confirmation": confirmation_schema.dump(user.confirmation)
        }, 200

    @classmethod
    def post(cls, user_id):
        """Resend confirmations"""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext('user_not_found')}, 404
        try:
            confirmation = user.most_recent_confirmation
            if confirmation:  # confirmation exists
                if confirmation.confirmed:  # already confirmed
                    return {"message": gettext("confirmation_already_confirmed")}
                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()

            # user.send_confirmation_email()

            return {"message": gettext("confirmation_resend_successful")}, 201
        except:
            traceback.print_exc()
            return {"message": gettext("confirmation_resend_fail")}
