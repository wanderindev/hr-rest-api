from unittest import TestCase

from app import create_app
from db import db

app = create_app('testing')


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        with app.app_context():
            db.create_all()

        self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
