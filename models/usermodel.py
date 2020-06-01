from datetime import datetime
from typing import List
from uuid import uuid4

from werkzeug.security import check_password_hash

from db import db
from models.confirmation import ConfirmationModel


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(40))
    email = db.Column(db.String(80), nullable=True, unique=True)
    password = db.Column(db.String(100), nullable=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    phonenumber = db.Column(db.String(15))
    address = db.Column(db.String(80))
    age = db.Column(db.Integer)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = uuid4().hex

    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()
    
    @property
    def fullname(self):
        return f'{self.firstname} {self.lastname}'.title()

    @classmethod
    def find_by_id(cls, _id) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_userid(cls, user_id) -> "UserModel":
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        self.save_to_db()

    @classmethod
    def is_login_valid(cls, user, password):
        # Check if user exists and validate password
        if user and check_password_hash(user.password, password):
            return True
        return False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
