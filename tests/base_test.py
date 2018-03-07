import json

from unittest import TestCase
from werkzeug.security import generate_password_hash

from app import create_app
from db import db
from models.bank_account import BankAccountModel
from models.department import DepartmentModel
from models.dependent import DependentModel
from models.emergency_contact import EmergencyContactModel
from models.employee import EmployeeModel
from models.employment_position import EmploymentPositionModel
from models.health_permit import HealthPermitModel
from models.organization import OrganizationModel
from models.passport import PassportModel
from models.schedule import ScheduleModel
from models.shift import ShiftModel
from models.uniform_item import UniformItemModel
from models.uniform_requirement import UniformRequirementModel
from models.uniform_size import UniformSizeModel
from models.user import AppUserModel

app = create_app('testing')


# noinspection PyTypeChecker
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
        """Create all db tables and two users before each test."""
        self.app = app.test_client
        self.app_context = app.app_context

        with self.app_context():
            db.create_all()

            self.u = self.get_user()

            self.other_u = self.get_user({
                'username': 'test_other_u',
                'password_hash': generate_password_hash('test_p'),
                'email': 'test_other_u@test_o.com',
                'organization_id': 1,
                'is_super': False,
                'is_owner': True,
                'is_active': True
            })

    def tearDown(self):
        """
        Delete all rows in all tables, except for the seed organization
        and seed user, after every test.
        """
        with app.app_context():
            db.session.remove()
            AppUserModel.query.filter(AppUserModel.id != 1).delete()
            BankAccountModel.query.delete()
            EmergencyContactModel.query.delete()
            DependentModel.query.delete()
            HealthPermitModel.query.delete()
            PassportModel.query.delete()
            UniformRequirementModel.query.delete()
            ScheduleModel.query.delete()
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

        Returns:
            The request headers.
        """
        with self.app() as c:
            with self.app_context():
                u = user or {'username': 'test_u', 'password': 'test_p'}

                # Send request to auth endpoint.
                r = c.post('/auth', data=json.dumps(u),
                           headers={'Content-Type': 'application/json'})

                return {
                    'Content-Type': 'application/json',
                    'Authorization': 'JWT ' + json.loads(r.data)['access_token']
                }

    # TODO: check if it is still used.
    @staticmethod
    def toggle_is_super(user=None):
        u = user or AppUserModel.find_by_id(1)
        u.is_super = not u.is_super
        u.save_to_db()

    @staticmethod
    def get_object(model, _dict):
        o = model.query.filter_by(**_dict).first()

        if o:
            return o

        if model is AppUserModel:
            o = model(password='test_p', **_dict)
        else:
            o = model(**_dict)

        o.save_to_db()

        return model.query.filter_by(**_dict).first()

    def get_organization(self, _dict=None):
        with self.app_context():
            _dict = _dict or {'organization_name': 'test_o', 'is_active': True}

            return self.get_object(OrganizationModel, _dict)

    def get_user(self, _dict=None):
        with self.app_context():
            _dict = _dict or {
                'username': 'test_u',
                'email': 'test_u@test_o.com',
                'organization_id': self.get_organization().id,
                'is_super': True,
                'is_owner': True,
                'is_active': True
            }
            _dict['password_hash'] = generate_password_hash(
                _dict.pop('password', 'test_p'))
            return self.get_object(AppUserModel, _dict)

    def get_department(self, _dict=None):
        with self.app_context():
            _dict = _dict or {
                'department_name': 'test_d',
                'organization_id': self.get_organization().id,
                'is_active': True
            }

            return self.get_object(DepartmentModel, _dict)

    def get_shift(self, _dict=None):
        with self.app_context():
            _dict = _dict or {
                'shift_name': 'test_s_r',
                'weekly_hours': 48,
                'is_rotating': True,
                'payment_period': 'Quincenal',
                'break_length': '00:30:00',
                'is_break_included_in_shift': False,
                'is_active': True,
                'organization_id': self.get_organization().id,
                'rotation_start_hour': '06:00:00',
                'rotation_end_hour': '21:00:00'
            }

            return self.get_object(ShiftModel, _dict)

    def get_employment_position(self, _dict=None):
        with self.app_context():
            _dict = _dict or {
                'position_name_feminine': 'test_e_p_f',
                'position_name_masculine': 'test_e_p_m',
                'minimum_hourly_wage': 1.00,
                'is_active': True,
                'organization_id': self.get_organization().id
            }

            return self.get_object(EmploymentPositionModel, _dict)

    def get_employee(self, _dict=None):
        with self.app_context():
            _dict = _dict or {
                'first_name': 'f_n',
                'second_name': 's_n',
                'first_surname': 'f_sn',
                'second_surname': 's_sn',
                'national_id_number': '1-11-111',
                'is_panamanian': True,
                'date_of_birth': '2000-01-31',
                'gender': 'Hombre',
                'address': 'Panamá',
                'home_phone': '222-2222',
                'mobile_phone': '6666-6666',
                'email': 'f_n@f_sn.com',
                'type_of_contract': 'Definido',
                'employment_date': '2018-01-01',
                'contract_expiration_date': '2018-01-31',
                'termination_date': '2018-01-15',
                'termination_reason': 'Período de Prueba',
                'salary_per_payment_period': 104,
                'representation_expenses_per_payment_period': 0,
                'payment_method': 'ACH',
                'is_active': True,
                'marital_status_id': 1,
                'department_id': self.get_department().id,
                'position_id': self.get_employment_position().id,
                'shift_id': self.get_shift().id
            }

            return self.get_object(EmployeeModel, _dict)

    def get_emergency_contact(self, _dict=None):
        with self.app_context():
            _dict = _dict or {
                'first_name': 'f_n',
                'last_name': 'l_n',
                'home_phone': '111-1111',
                'work_phone': '222-2222',
                'mobile_phone': '6666-6666',
                'employee_id': self.get_employee().id
            }

            return self.get_object(EmergencyContactModel, _dict)

    def get_health_permit(self, _dict=None):
        with self.app_context():
            _dict = _dict or {
                'health_permit_type': 'Verde',
                'issue_date': '2018-01-01',
                'expiration_date': '2019-01-01',
                'employee_id': self.get_employee().id
            }

            return self.get_object(HealthPermitModel, _dict)

    def get_passport(self, _dict=None):
        with self.app_context():
            _dict = _dict or {
                'passport_number': '123456',
                'issue_date': '2018-01-01',
                'expiration_date': '2019-01-01',
                'employee_id': self.get_employee().id,
                'country_id': 1
            }

            return self.get_object(PassportModel, _dict)

    def get_uniform_item(self, organization_id):
        with self.app_context():
            u_i = UniformItemModel('test_u_i', organization_id)
            u_i.save_to_db()

            return UniformItemModel.find_by_id(u_i.id, organization_id)

    def get_uniform_size(self, item_id, organization_id):
        with self.app_context():
            u_s = UniformSizeModel('test_u_s', item_id)
            u_s.save_to_db()

            return UniformSizeModel.find_by_id(u_s.id, organization_id)

    def get_uniform_requirement(self, employee_id, item_id,
                                size_id, organization_id):
        with self.app_context():
            u_r = UniformRequirementModel(employee_id, item_id, size_id)
            u_r.save_to_db()

            return UniformRequirementModel.find_by_id(u_r.id, organization_id)

    def get_bank_account(self, _dict=None):
        with self.app_context():
            with self.app_context():
                _dict = _dict or {
                    'account_number': '1234',
                    'account_type': 'Corriente',
                    'is_active': True,
                    'employee_id': self.get_employee().id,
                    'bank_id': 1
                }

            return self.get_object(BankAccountModel, _dict)

    def get_dependent(self, _dict=None):
        with self.app_context():
            _dict = _dict or {
                'first_name': 'f_n',
                'second_name': 's_n',
                'first_surname': 'f_sn',
                'second_surname': 's_sn',
                'gender': 'Mujer',
                'date_of_birth': '2018-01-01',
                'employee_id': self.get_employee().id,
                'family_relation_id': 1
            }

            return self.get_object(DependentModel, _dict)

    def get_schedule(self, _dict=None):
        with self.app_context():
            _dict = _dict or {
                'start_date': '2018-01-01',
                'department_id': self.get_department().id
            }

            return self.get_object(ScheduleModel, _dict)
