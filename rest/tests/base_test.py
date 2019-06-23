import json

from unittest import TestCase
from werkzeug.security import check_password_hash

from rest.app import create_app
from db import db
from models.attendance import AttendanceModel
from models.bank_account import BankAccountModel
from models.creditor import CreditorModel
from models.deduction import DeductionModel
from models.deduction_detail import DeductionDetailModel
from models.department import DepartmentModel
from models.dependent import DependentModel
from models.emergency_contact import EmergencyContactModel
from models.employee import EmployeeModel
from models.employment_position import EmploymentPositionModel
from models.health_permit import HealthPermitModel
from models.organization import OrganizationModel
from models.passport import PassportModel
from models.payment import PaymentModel
from models.payment_detail import PaymentDetailModel
from models.raw_attendance import RawAttendanceModel
from models.schedule import ScheduleModel
from models.schedule_detail import ScheduleDetailModel
from models.shift import ShiftModel
from models.uniform_item import UniformItemModel
from models.uniform_requirement import UniformRequirementModel
from models.uniform_size import UniformSizeModel
from models.user import AppUserModel

app = create_app('testing')


# noinspection PyTypeChecker
class BaseTest(TestCase):
    """Base class which is inherited by all system test classes."""
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
        self.client = app.test_client
        self.app_context = app.app_context

        with self.app_context():
            db.create_all()

    def tearDown(self):
        """Clear db tables after each test"""
        with self.app_context():
            self.clear_db()

    @staticmethod
    def clear_db():
        """
        Delete all rows in all tables, except for the seed organization
        and seed user.  It is called on tearDown and also after all subTest.
        """
        db.session.remove()
        AppUserModel.query.filter(AppUserModel.id != 1).delete()
        BankAccountModel.query.delete()
        EmergencyContactModel.query.delete()
        DependentModel.query.delete()
        HealthPermitModel.query.delete()
        PassportModel.query.delete()
        UniformRequirementModel.query.delete()
        ScheduleDetailModel.query.delete()
        ScheduleModel.query.delete()
        DeductionDetailModel.query.delete()
        DeductionModel.query.delete()
        CreditorModel.query.delete()
        PaymentDetailModel.query.delete()
        PaymentModel.query.delete()
        AttendanceModel.query.delete()
        RawAttendanceModel.query.delete()
        EmployeeModel.query.delete()
        EmploymentPositionModel.query.delete()
        ShiftModel.query.delete()
        UniformSizeModel.query.delete()
        UniformItemModel.query.delete()
        DepartmentModel.query.delete()
        OrganizationModel.query.filter(OrganizationModel.id != 1).delete()
        db.session.commit()

    def get_headers(self, user=None):
        """
        Authenticate user and return request headers that include
        the authorization JWT.

        All endpoints requires an authorization header with a
        JWT access token.  This method authenticates the user
        and returns correct headers.

        :param user: A dictionary with a username and a password
        :type user: dict
        Returns:
            The authorization headers.
        """
        with self.client() as c:
            with self.app_context():
                u = user or {'username': 'test_u', 'password': 'test_p'}

                try:
                    result = c.post('/auth',
                                    data=json.dumps(u),
                                    headers={
                                        'Content-Type': 'application/json'
                                    })
                    return {
                        'Content-Type': 'application/json',
                        'Authorization': 'JWT ' +
                                         json.loads(result.data)[
                                             'access_token'
                                         ]
                    }
                except KeyError:
                    # Returns fake token for testing purposes if user
                    # is not in the database.
                    return {
                        'Content-Type': 'application/json',
                        'Authorization': 'JWT FaKeToKeN!!'
                    }

    def check_record(self, data_sent, data_received, parsed_model=None,
                     orig_data=None):
        """
        Assert that all columns in a record contain the expected values.

        This method compares key by key the dictionary containing the values
        sent to the resources endpoint with the dictionary cotaining the
        values returned by the endpoint. If any value does not match, an
        exception is raised and the subtest fails.

        Some models do not allow certain column values to change after record
        creation.  The names of these columns are included in the
        exclude_from_update property of the model. For this reason, when
        checking PUT requests, the values of any keys included in
        exclude_from_update are checked against the original value and
        not the value sent in the payload of the PUT request.

        :param data_sent: A dictionary with the values sent to the
            resources endpoint
        :param data_received: A dictionary with the values returned
            by the endpoint
        :param parsed_model: A dictionary with the model's metadata
        :param orig_data: A dictionary with the values used to
            instantiate the model
        :type data_sent: dict
        :type data_received: dict
        :type parsed_model: dict
        :type orig_data: dict
        """
        for k, v in data_sent.items():
            if orig_data and k in parsed_model['excluded']:
                data_sent[k] = orig_data[k]

                if k == 'password':
                    self.assertTrue(check_password_hash(
                        data_received['password_hash'], v))
                else:
                    self.compare_item(data_sent[k], data_received[k])

    def compare_item(self, item_1, item_2):
        """
        Asserts that item_1 and item_2 are equal.

        Since item_2 may come from the json returned by a request to
        an empoint, it it necessary to cast it to the appropriate type
        before doing the assertion.

        :param item_1: A value sent to an endpoint or a model
        :param item_2: A value returned from an endpoint or a model
        """
        if type(item_1) == int:
            self.assertEqual(int(item_2), item_1)
        elif type(item_1) == float:
            self.assertEqual(float(item_2), item_1)
        elif type(item_1) == bool and item_1:
            self.assertTrue(item_2)
        elif type(item_1) == bool and not item_1:
            self.assertFalse(item_2)
        else:
            self.assertEqual(item_2, item_1)
