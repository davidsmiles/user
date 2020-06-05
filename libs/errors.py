from flask_restful import HTTPException
from libs.strings import gettext


class UserEmailExists(HTTPException):
    pass


class UserNotExist(HTTPException):
    pass


class QueryInvalidError(HTTPException):
    pass


class InternalServerError(HTTPException):
    pass


class SchemaValidationError(HTTPException):
    pass


class UnauthorizedError(HTTPException):
    pass


errors = {
    "UserEmailExists": {
        "message": gettext("user_email_exists"),
        "status": 400
    },
    "UserNotExist": {
        "message": gettext("user_not_found"),
        "status": 404
    },
    "UnauthorizedError": {
        "message": gettext("user_invalid_credentials"),
        "status": 401
    },
    "QueryInvalidError": {
        "message": gettext('unexpected_user_data'),
        "status": 500
    },
    "InternalServerError": {
        "message": "Oops, something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    }
}