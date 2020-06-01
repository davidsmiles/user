from datetime import datetime

from db import db
from models.usermodel import UserModel


class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    phonenumber = db.Column(db.String(15))
    address = db.Column(db.String(80))
    age = db.Column(db.Integer)

    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @property
    def fullname(self):
        return f'{self.firstname} {self.lastname}'.title()

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
