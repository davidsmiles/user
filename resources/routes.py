# Resources
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.signup import AccountSignUp
from resources.login import AccountLogin
from resources.user import User
from resources.useridentity import UserIdentity
from resources.users import Users


def initialize_routes(api):
    # User
    api.add_resource(User, '/users/<string:user_id>')
    api.add_resource(Users, '/users')
    api.add_resource(UserIdentity, '/users/identify/<string:user_id>')

    # Account
    api.add_resource(AccountSignUp, '/accounts/signup')
    api.add_resource(AccountLogin, '/accounts/login')
    api.add_resource(Confirmation, '/accounts/confirmation/<string:confirmation_id>')
    api.add_resource(ConfirmationByUser, '/accounts/confirmation/user/<string:user_id>')