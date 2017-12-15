from unittest import TestCase

from app import create_app
from db import db

app = create_app('testing')


class BaseTest(TestCase):
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

        self.app_context = app.app_context

    def tearDown(self):
        """Drop all db tables after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()
