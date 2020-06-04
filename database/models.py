from flask_bcrypt import generate_password_hash, check_password_hash
from extensions import db


class Address(db.EmbeddedDocument):

    firstname = db.StringField()
    lastname = db.StringField()
    company = db.StringField()
    address1 = db.StringField()
    address2 = db.StringField()
    city = db.StringField()
    state = db.StringField()
    country = db.StringField()
    postal_or_zip_code = db.IntField()


class Users(db.Document):

    firstname = db.StringField(required=True)
    lastname = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    address = db.ListField(db.EmbeddedDocumentField(Address))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
