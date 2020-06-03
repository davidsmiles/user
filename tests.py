import unittest

from flask_testing import TestCase
from werkzeug.security import generate_password_hash


from app import app, api
from extensions import *

from models.usermodel import UserModel
from resources.routes import initialize_routes


# Initialize
initialize_extensions(app)
initialize_routes(api)


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(
            UserModel(
                firstname='david',
                lastname='smiles',
                email='ugberodavid@gmail.com',
                password=generate_password_hash('pass')
            )
        )
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UserTestCase(BaseTestCase):

    def test_index(self):
        response = self.client.get('/', content_type='text/html')
        self.assertEqual(response.status_code, 404)

    def test_user_signup(self):
        response = self.client.post('/accounts/signup',
                                    json={
                                        'firstname': 'david',
                                        'lastname': 'smiles',
                                        'email': 'davidsmiles@gmail.com',
                                        'password': 'pass'
                                    })
        self.assert_200(response)

    def test_user_login(self):
        response = self.client.post('/accounts/login',
                                    json={
                                         'email': 'ugberodavid@gmail.com',
                                         'password': 'pass'
                                     }
                                    )
        self.assert_200(response)

    def test_get_user(self):
        response = self.client.get('/users/1')
        self.assert200(response)
    
    def test_update_user(self):
        response = self.client.put('/users/1',
                                    json={
                                         'firstname': 'david',
                                        'lastname': 'smiles'
                                     }
                                    )
        self.assertStatus(response, 200)

    def test_delete_user(self):
        response = self.client.delete('/users/1')
        self.assertStatus(response, 204)

    def test_get_all_users(self):
        response = self.client.get('/users')
        self.assert_200(response)


if __name__ == '__main__':
    unittest.main()
