from ma import ma
from models.usermodel import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        load_only = ('password', 'id')

    profile = ma.URLFor("profile", user_id="<id>")