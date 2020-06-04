# Resources
from resources.address import Address
from resources.signup import AccountSignUp
from resources.login import AccountLogin
from resources.user import User
from resources.users import AllUsers


def initialize_routes(api):
    # User
    api.add_resource(User, '/users/<string:id>')
    api.add_resource(AllUsers, '/users')

    # Account
    api.add_resource(AccountSignUp, '/account/register')
    api.add_resource(AccountLogin, '/account/login')
    api.add_resource(Address, '/account/addresses')