import json

from unittest import TestCase

from app import create_app
from db import db

app = create_app('testing')


class BaseTest(TestCase):
    """
    Base class which is inherited by all
    integration and system test classes.
    """
    @classmethod
    def setUpClass(cls):
        """
        Register the flask_sqlalchemy extension at
        the beginning of the test suite.
        """
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        """Create all db tables before each test."""
        with app.app_context():
            db.create_all()

        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        """Drop all db tables after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def authorize(self):
        """
        Authenticate user and return the authorization header.

        Some endpoints requires an authorization header with a
        JWT access token.  This method authenticates the user
        and returns the authorization header.

        Returns:
            An authorization header.
        """
        with self.app() as c:
            with self.app_context():
                # Register the user.
                c.post('/user', data=self.u_dict)

                r = c.post('/auth', data=json.dumps({
                    'username': 'javier',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})

                return {
                    'Authorization': "JWT " + json.loads(r.data)["access_token"]
                }
