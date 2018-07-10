import json

from unittest import TestCase
from werkzeug.security import generate_password_hash

from app import create_app
from db import db
from models.bank_account import BankAccountModel
from models.country import CountryModel
from models.creditor import CreditorModel
from models.deduction import DeductionModel
from models.deduction_detail import DeductionDetailModel
from models.department import DepartmentModel
from models.dependent import DependentModel
from models.emergency_contact import EmergencyContactModel
from models.employee import EmployeeModel
from models.employment_position import EmploymentPositionModel
from models.health_permit import HealthPermitModel
from models.marital_status import MaritalStatusModel
from models.organization import OrganizationModel
from models.passport import PassportModel
from models.payment import PaymentModel
from models.payment_detail import PaymentDetailModel
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
                                         json.loads(result.data)['access_token']
                    }
                except Exception as e:
                    # Returns fake token for testing purposes if user
                    # is not in the database.
                    print(e)
                    return {
                        'Content-Type': 'application/json',
                        'Authorization': 'JWT FaKeToKeN!!'
                    }

    def set_test_users(self):
        """Set up dicts with credentials for test users"""
        with self.app_context():
            self.test_user = {
                'username': 'test_u',
                'password': 'test_p'
            }

            self.other_test_user = {
                'username': 'test_other_u',
                'password': 'test_p'
            }

            self.fake_user = {
                'username': 'fake_u',
                'password': 'fake_p'
            }

            self.root_user = {
                'username': 'jfeliu',
                'password': '1234'
            }

    def create_users(self):
        """Add users to the database"""
        with self.app_context():
            self.set_test_users()
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

    def get_test_user(self, user_type):
        if user_type is 'root':
            self.set_test_users()
            return self.root_user
        elif user_type is 'test':
            self.create_users()
            return self.test_user
        elif user_type is 'other':
            self.create_users()
            return self.other_test_user
        elif user_type is 'fake':
            self.set_test_users()
            return self.fake_user

    def check_record(self, expected, record, parsed_model):
        """Assert that all columns in a record contain the expected values"""
        for key in parsed_model['keys']:
            if record[key] is not None:
                if key in parsed_model['int']:
                    self.assertEqual(expected[key], int(record[key]))
                elif key in parsed_model['float']:
                    self.assertEqual(expected[key], float(record[key]))
                elif key in parsed_model['bool'] and expected[key]:
                    self.assertTrue(record[key])
                elif key in parsed_model['bool'] and not expected[key]:
                    self.assertFalse(record[key])
                else:
                    self.assertEqual(expected[key], record[key])

    def get_system_test_params(self):
        return [
            (
                'Organization Resource',
                OrganizationModel,
                (
                    {
                        'organization_name': 'test_o',
                        'is_active': True
                    },
                    {
                        'organization_name': 'new_test_o',
                        'is_active': False
                    }
                ),
                'organization',
                'root'
            ),
            (
                'Department Resource',
                DepartmentModel,
                (
                    {
                        'department_name': 'test_d',
                        'organization_id': self.get_organization,
                        'is_active': True
                    },
                    {
                        'department_name': 'new_test_d',
                        'organization_id': self.get_organization,
                        'is_active': True
                    }
                ),
                'department',
                'test'
            ),
            (
                'MaritalStatus Resource',
                MaritalStatusModel,
                None,
                'marital_statuses',
                'test'
            ),
            (
                'EmploymentPosition Resource',
                EmploymentPositionModel,
                (
                    {
                        'position_name_feminine': 'test_e_p_f',
                        'position_name_masculine': 'test_e_p_m',
                        'minimum_hourly_wage': 1.00,
                        'is_active': True,
                        'organization_id': self.get_organization,
                    },
                    {
                        'position_name_feminine': 'new_test_e_p_f',
                        'position_name_masculine': 'new_test_e_p_m',
                        'minimum_hourly_wage': 2.00,
                        'is_active': True,
                        'organization_id': self.get_organization,
                    }
                ),
                'employment_position',
                'test'
            ),
            (
                'Shift Resource - Rotating',
                ShiftModel,
                (
                    {
                        'shift_name': 'test_s_r',
                        'weekly_hours': 48,
                        'is_rotating': True,
                        'payment_period': 'Quincenal',
                        'break_length': '00:30:00',
                        'is_break_included_in_shift': False,
                        'is_active': True,
                        'organization_id': self.get_organization,
                        'rotation_start_hour': '06:00:00',
                        'rotation_end_hour': '21:00:00'
                    },
                    {
                        'shift_name': 'new_test_s_r',
                        'weekly_hours': 44,
                        'is_rotating': True,
                        'payment_period': 'Semanal',
                        'break_length': '01:00:00',
                        'is_break_included_in_shift': True,
                        'is_active': True,
                        'organization_id': self.get_organization,
                        'rotation_start_hour': '00:00:00',
                        'rotation_end_hour': '15:00:00'
                    }
                ),
                'shift',
                'test'
            ),
            (
                'Shift Resource - Fixed',
                ShiftModel,
                (
                    {
                        'shift_name': 'test_s_f',
                        'weekly_hours': 44,
                        'is_rotating': False,
                        'payment_period': 'Quincenal',
                        'break_length': '00:30:00',
                        'is_break_included_in_shift': False,
                        'is_active': True,
                        'organization_id': self.get_organization,
                        'fixed_start_hour_monday': '08:00:00',
                        'fixed_start_break_hour_monday': '12:00:00',
                        'fixed_end_break_hour_monday': '12:30:00',
                        'fixed_end_hour_monday': '16:30:00',
                        'fixed_start_hour_tuesday': '08:00:00',
                        'fixed_start_break_hour_tuesday': '12:00:00',
                        'fixed_end_break_hour_tuesday': '12:30:00',
                        'fixed_end_hour_tuesday': '16:30:00',
                        'fixed_start_hour_wednesday': '08:00:00',
                        'fixed_start_break_hour_wednesday': '12:00:00',
                        'fixed_end_break_hour_wednesday': '12:30:00',
                        'fixed_end_hour_wednesday': '16:30:00',
                        'fixed_start_hour_thursday': '08:00:00',
                        'fixed_start_break_hour_thursday': '12:00:00',
                        'fixed_end_break_hour_thursday': '12:30:00',
                        'fixed_end_hour_thursday': '16:30:00',
                        'fixed_start_hour_friday': '08:00:00',
                        'fixed_start_break_hour_friday': '12:00:00',
                        'fixed_end_break_hour_friday': '12:30:00',
                        'fixed_end_hour_friday': '16:30:00',
                        'fixed_start_hour_saturday': '08:00:00',
                        'fixed_end_hour_saturday': '12:00:00',
                        'rest_day': 'Domingo'
                    },
                    {
                        'shift_name': 'new_test_s_f',
                        'weekly_hours': 48,
                        'is_rotating': False,
                        'payment_period': 'Diario',
                        'break_length': '00:30:00',
                        'is_break_included_in_shift': False,
                        'is_active': True,
                        'organization_id': self.get_organization,
                        'fixed_start_hour_sunday': '09:00:00',
                        'fixed_start_break_hour_sunday': '13:00:00',
                        'fixed_end_break_hour_sunday': '13:30:00',
                        'fixed_end_hour_sunday': '17:30:00',
                        'fixed_start_hour_monday': '09:00:00',
                        'fixed_start_break_hour_monday': '13:00:00',
                        'fixed_end_break_hour_monday': '13:30:00',
                        'fixed_end_hour_monday': '17:30:00',
                        'fixed_start_hour_tuesday': '09:00:00',
                        'fixed_start_break_hour_tuesday': '13:00:00',
                        'fixed_end_break_hour_tuesday': '13:30:00',
                        'fixed_end_hour_tuesday': '17:30:00',
                        'fixed_start_hour_wednesday': '09:00:00',
                        'fixed_start_break_hour_wednesday': '13:00:00',
                        'fixed_end_break_hour_wednesday': '13:30:00',
                        'fixed_end_hour_wednesday': '17:30:00',
                        'fixed_start_hour_thursday': '09:00:00',
                        'fixed_start_break_hour_thursday': '13:00:00',
                        'fixed_end_break_hour_thursday': '13:30:00',
                        'fixed_end_hour_thursday': '17:30:00',
                        'fixed_start_hour_friday': '09:00:00',
                        'fixed_start_break_hour_friday': '13:00:00',
                        'fixed_end_break_hour_friday': '13:30:00',
                        'fixed_end_hour_friday': '17:30:00',
                        'fixed_start_hour_saturday': None,
                        'fixed_end_hour_saturday': None,
                        'rest_day': 'Sábado'
                    }
                ),
                'shift',
                'test'
            ),
            (
                'Employee Resource',
                EmployeeModel,
                (
                    {
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
                        'department_id': self.get_department,
                        'position_id': self.get_employment_position,
                        'shift_id': self.get_shift
                    },
                    {
                        'first_name': 'new_f_n',
                        'second_name': 'new_s_n',
                        'first_surname': 'new_f_sn',
                        'second_surname': 'new_s_sn',
                        'national_id_number': 'N-1-11-111',
                        'is_panamanian': False,
                        'date_of_birth': '2001-01-31',
                        'gender': 'Mujer',
                        'address': 'Chiriquí',
                        'home_phone': '333-3333',
                        'mobile_phone': '6666-7777',
                        'email': 'new_f_n@new_f_sn.com',
                        'type_of_contract': 'Indefinido',
                        'employment_date': '2019-01-01',
                        'contract_expiration_date': '2019-01-31',
                        'termination_date': '2019-01-15',
                        'termination_reason': 'Renuncia',
                        'salary_per_payment_period': 208,
                        'representation_expenses_per_payment_period': 100,
                        'payment_method': 'Cheque',
                        'is_active': True,
                        'marital_status_id': 2,
                        'department_id': self.get_department,
                        'position_id': self.get_employment_position,
                        'shift_id': self.get_shift
                    }
                ),
                'employee',
                'test'
            ),
            (
                'HealthPermit Resource',
                HealthPermitModel,
                (
                    {
                        'health_permit_type': 'Verde',
                        'issue_date': '2018-01-01',
                        'expiration_date': '2019-01-01',
                        'employee_id': self.get_employee
                    },
                    {
                        'health_permit_type': 'Blanco',
                        'issue_date': '2018-01-31',
                        'expiration_date': '2019-01-31',
                        'employee_id': self.get_employee
                    }
                ),
                'health_permit',
                'test'
            ),
            (
                'EmergencyContact Resource',
                EmergencyContactModel,
                (
                    {
                        'first_name': 'f_n',
                        'last_name': 'l_n',
                        'home_phone': '111-1111',
                        'work_phone': '222-2222',
                        'mobile_phone': '6666-6666',
                        'employee_id': self.get_employee
                    },
                    {
                        'first_name': 'new_f_n',
                        'last_name': 'new_l_n',
                        'home_phone': '333-3333',
                        'work_phone': '444-4444',
                        'mobile_phone': '6666-7777',
                        'employee_id': self.get_employee
                    }
                ),
                'emergency_contact',
                'test'
            ),
            (
                'Country Resource',
                CountryModel,
                None,
                'countries',
                'test'
            ),
            (
                'Passport Resource',
                PassportModel,
                (
                    {
                        'passport_number': '123456',
                        'issue_date': '2018-01-01',
                        'expiration_date': '2019-01-01',
                        'employee_id': self.get_employee,
                        'country_id': 1
                    },
                    {
                        'passport_number': '654321',
                        'issue_date': '2018-01-31',
                        'expiration_date': '2019-01-31',
                        'employee_id': self.get_employee,
                        'country_id': 2
                    }
                ),
                'passport',
                'test'
            ),
            (
                'UniformItem Resource',
                UniformItemModel,
                (
                    {
                        'item_name': 'test_u_i',
                        'organization_id': self.get_organization
                    },
                    {
                        'item_name': 'new_test_u_i',
                        'organization_id': self.get_organization
                    }
                ),
                'uniform_item',
                'test'
            ),
            (
                'UniformSize Resource',
                UniformSizeModel,
                (
                    {
                        'size_description': 'test_u_s',
                        'uniform_item_id': self.get_uniform_item
                    },
                    {
                        'size_description': 'new_test_u_s',
                        'uniform_item_id': self.get_uniform_item
                    }
                ),
                'uniform_size',
                'test'
            ),
            (
                'UniformRequirement Resource',
                UniformRequirementModel,
                (
                    {
                        'employee_id': self.get_employee,
                        'uniform_item_id': self.get_uniform_item,
                        'uniform_size_id': self.get_uniform_size
                    },
                    {
                        'employee_id': self.get_employee,
                        'uniform_item_id': self.get_uniform_item,
                        'uniform_size_id': self.get_uniform_size
                    }
                ),
                'uniform_requirement',
                'test'
            ),
            (
                'Bank Resource',
                UniformRequirementModel,
                None,
                'banks',
                'test'
            )
        ]

    @staticmethod
    def get_b_object(b_obj):
        if b_obj is not None:
            for _obj in b_obj:
                for k, v in _obj.items():
                    if callable(v):
                        _obj[k] = v().id

            return b_obj

        return None, None

    # TODO: check if it is still used.
    @staticmethod
    def toggle_is_super(user=None):
        u = user or AppUserModel.find_by_id(1)
        u.is_super = not u.is_super
        u.save_to_db()

    @staticmethod
    def get_object(model, _dict):
        """
        Return an object from the database if it exists.  Create
        and return the object if it does not exists
        """
        if model is AppUserModel:
            o = model.query.filter_by(username=_dict['username']).first()
            if o:
                return o
            else:
                o = model(password='test_p', **_dict)
        else:
            o = model.query.filter_by(**_dict).first()
            if o:
                return o
            else:
                o = model(**_dict)

        o.save_to_db()

        return model.query.filter_by(**_dict).first()

    def get_organization(self, _dict=None):
        """Create and return an organization object"""
        with self.app_context():
            _dict = _dict or {'organization_name': 'test_o', 'is_active': True}

            return self.get_object(OrganizationModel, _dict)

    def get_user(self, _dict=None):
        """Create and return a user object"""
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
        """Create and return a department object"""
        with self.app_context():
            _dict = _dict or {
                'department_name': 'test_d',
                'organization_id': self.get_organization().id,
                'is_active': True
            }

            return self.get_object(DepartmentModel, _dict)

    def get_shift(self, _dict=None):
        """Create and return a shift object"""
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
        """Create and return an employment_position object"""
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
        """Create and return an employee object"""
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
        """Create and return an emergency_contact object"""
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
        """Create and return a health_permit object"""
        with self.app_context():
            _dict = _dict or {
                'health_permit_type': 'Verde',
                'issue_date': '2018-01-01',
                'expiration_date': '2019-01-01',
                'employee_id': self.get_employee().id
            }

            return self.get_object(HealthPermitModel, _dict)

    def get_passport(self, _dict=None):
        """Create and return a passport object"""
        with self.app_context():
            _dict = _dict or {
                'passport_number': '123456',
                'issue_date': '2018-01-01',
                'expiration_date': '2019-01-01',
                'employee_id': self.get_employee().id,
                'country_id': 1
            }

            return self.get_object(PassportModel, _dict)

    def get_uniform_item(self, _dict=None):
        """Create and return a uniform_item object"""
        with self.app_context():
            _dict = _dict or {
                'item_name': 'test_u_i',
                'organization_id': self.get_organization().id
            }

            return self.get_object(UniformItemModel, _dict)

    def get_uniform_size(self, _dict=None):
        """Create and return a uniform_size object"""
        with self.app_context():
            with self.app_context():
                _dict = _dict or {
                    'size_description': 'test_u_s',
                    'uniform_item_id': self.get_uniform_item().id
                }

                return self.get_object(UniformSizeModel, _dict)

    def get_uniform_requirement(self, _dict=None):
        """Create and return a uniform_requirement object"""
        with self.app_context():
            _dict = _dict or {
                'employee_id': self.get_employee().id,
                'uniform_item_id': self.get_uniform_item().id,
                'uniform_size_id': self.get_uniform_size().id
            }

            return self.get_object(UniformRequirementModel, _dict)

    def get_bank_account(self, _dict=None):
        """Create and return a bank_account object"""
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
        """Create and return a dependent object"""
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
        """Create and return a schedule object"""
        with self.app_context():
            _dict = _dict or {
                'start_date': '2018-01-01',
                'department_id': self.get_department().id
            }

            return self.get_object(ScheduleModel, _dict)

    def get_schedule_detail(self, _dict=None):
        """Create and return a schedule_detail object"""
        with self.app_context():
            _dict = _dict or {
                'day_1_start': '2018-01-01T06:00:00',
                'day_1_end': '2018-01-01T14:00:00',
                'day_1_comment': 'comment 1',
                'day_2_start': '2018-01-02T06:00:00',
                'day_2_end': '2018-01-02T14:00:00',
                'day_2_comment': 'comment 2',
                'day_3_start': '2018-01-03T06:00:00',
                'day_3_end': '2018-01-03T14:00:00',
                'day_3_comment': 'comment 3',
                'day_4_start': '2018-01-04T06:00:00',
                'day_4_end': '2018-01-04T14:00:00',
                'day_4_comment': 'comment 4',
                'day_5_start': None,
                'day_5_end': None,
                'day_5_comment': None,
                'day_6_start': '2018-01-06T22:00:00',
                'day_6_end': '2018-01-07T06:00:00',
                'day_6_comment': 'comment 6',
                'day_7_start': '2018-01-07T22:00:00',
                'day_7_end': '2018-01-08T06:00:00',
                'day_7_comment': 'comment 7',
                'employee_id': self.get_employee().id,
                'schedule_id': self.get_schedule().id
            }
            return self.get_object(ScheduleDetailModel, _dict)

    def get_payment(self, _dict=None):
        """Create and return a payment object"""
        with self.app_context():
            _dict = _dict or {
                'payment_date': '2018-01-01',
                'document_number': '1234-abc',
                'employee_id': self.get_employee().id
            }

            return self.get_object(PaymentModel, _dict)

    def get_payment_detail(self, _dict=None):
        """Create and return a payment_detail object"""
        with self.app_context():
            _dict = _dict or {
                'payment_type': 'Salario Regular',
                'gross_payment': 1234.56,
                'ss_deduction': 123.45,
                'se_deduction': 12.34,
                'isr_deduction': 1.23,
                'payment_id': self.get_payment().id
            }

            return self.get_object(PaymentDetailModel, _dict)

    def get_creditor(self, _dict=None):
        """Create and return a creditor object"""
        with self.app_context():
            _dict = _dict or {
                'creditor_name': 'test_cr',
                'phone_number': '123-4567',
                'email': 'test@test_cr.com',
                'organization_id': self.get_organization().id,
                'is_active': True
            }

            return self.get_object(CreditorModel, _dict)

    def get_deduction(self, _dict=None):
        """Create and return a deduction object"""
        with self.app_context():
            _dict = _dict or {
                'start_date': '2018-01-01',
                'end_date': '2018-01-31',
                'deduction_per_payment_period': 123.45,
                'payment_method': 'Cheque',
                'deduct_in_december': True,
                'is_active': True,
                'employee_id': self.get_employee().id,
                'creditor_id': self.get_creditor().id
            }

            return self.get_object(DeductionModel, _dict)

    def get_deduction_detail(self, _dict=None):
        """Create and return a dedcution_detail object"""
        with self.app_context():
            _dict = _dict or {
                'deducted_amount': 67.89,
                'payment_id': self.get_payment().id,
                'deduction_id': self.get_deduction().id
            }

            return self.get_object(DeductionDetailModel, _dict)
