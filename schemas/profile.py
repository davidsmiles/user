from ma import ma
from models.profile import Profile


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        load_instance = True
        load_only = ('id',)
