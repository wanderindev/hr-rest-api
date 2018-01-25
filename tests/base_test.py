import json

from unittest import TestCase

from app import create_app
from db import db
from models.organization import OrganizationModel
from models.user import AppUserModel

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
            AppUserModel.query.filter(AppUserModel.id != 1).delete()
            OrganizationModel.query.filter(OrganizationModel.id != 1).delete()
            db.session.commit()

    def get_headers(self):
        """
        Authenticate user and return request headers that include
        the authorization JWT.

        All endpoints requires an authorization header with a
        JWT access token.  This method authenticates the user
        and returns correct headers.

        Returns:
            The request headers.
        """
        with self.app() as c:
            with self.app_context():
                # Send request to auth endpoint.
                r = c.post('/auth', data=json.dumps({
                    'username': 'jfeliu',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})

                return {
                    'Content-Type': 'application/json',
                    'Authorization': 'JWT ' + json.loads(r.data)['access_token']
                }
