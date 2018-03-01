from datetime import date, time
import json

from unittest import TestCase

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
                u = user or {'username': 'jfeliu', 'password': '1234'}

                # Send request to auth endpoint.
                r = c.post('/auth', data=json.dumps(u),
                           headers={'Content-Type': 'application/json'})

                return {
                    'Content-Type': 'application/json',
                    'Authorization': 'JWT ' + json.loads(r.data)['access_token']
                }

    @staticmethod
    def toggle_is_super(user=None):
        u = user or AppUserModel.find_by_id(1)
        u.is_super = not u.is_super
        u.save_to_db()

    def get_organization(self):
        with self.app_context():
            o = OrganizationModel('test_o', True)
            o.save_to_db()

            return OrganizationModel.query.filter_by(id=o.id).first()

    def get_organization_id(self, o_dict=None):
        with self.app() as c:
            with self.app_context():
                o = o_dict or {'organization_name': 'test_o', 'is_active': True}
                r = c.post('/organization',
                           data=json.dumps(o),
                           headers=self.get_headers())
                print(r.data)
                return json.loads(r.data)['organization']['id']

    def get_user(self, organization_id, is_super=True):
        with self.app_context():
            u = AppUserModel('test_u', 'test_p', 'test_u@test_o.com',
                             organization_id, is_super, True, True)
            u.save_to_db()

            return AppUserModel.find_by_id(u.id)

    def get_department(self, user):
        with self.app_context():
            d = DepartmentModel('test_d', user.organization_id, True)
            d.save_to_db()

            return DepartmentModel.find_by_id(d.id, user)

    def get_department_id(self, d_dict=None):
        with self.app() as c:
            with self.app_context():
                d = d_dict or {
                    'department_name': 'test_d',
                    'organization_id': 1,
                    'is_active': True
                }

                r = c.post('/department',
                           data=json.dumps(d),
                           headers=self.get_headers())

                return json.loads(r.data)['department']['id']

    def get_shift(self, user, organization_id=None):
        with self.app_context():
            organization_id = organization_id or user.organization_id

            s = ShiftModel('test_s_r', 48, True, 'Quincenal',
                           time(0, 30), False, True, organization_id,
                           rotation_start_hour=time(6),
                           rotation_end_hour=time(21))
            s.save_to_db()

            return ShiftModel.find_by_id(s.id, user)

    def get_shift_id(self, s_dict=None):
        with self.app() as c:
            with self.app_context():
                s = s_dict or {
                    'shift_name': 'test_s_r',
                    'weekly_hours': 48,
                    'is_rotating': True,
                    'payment_period': 'Quincenal',
                    'break_length': '00:30:00',
                    'is_break_included_in_shift': False,
                    'is_active': True,
                    'organization_id': 1,
                    'rotation_start_hour': '06:00:00',
                    'rotation_end_hour': '21:00:00'
                }

                r = c.post('/shift',
                           data=json.dumps(s),
                           headers=self.get_headers())

                return json.loads(r.data)['shift']['id']

    def get_employment_position(self, user, organization_id=None):
        with self.app_context():
            organization_id = organization_id or user.organization_id

            e_p = EmploymentPositionModel('test_e_p_f', 'test_e_p_m',
                                          1.00, True, organization_id)
            e_p.save_to_db()

            return EmploymentPositionModel.find_by_id(e_p.id, user)

    def get_employment_position_id(self, e_p_dict=None):
        with self.app() as c:
            with self.app_context():
                e_p = e_p_dict or {
                    'position_name_feminine': 'test_e_p_f',
                    'position_name_masculine': 'test_e_p_m',
                    'minimum_hourly_wage': 1.00,
                    'is_active': True,
                    'organization_id': 1
                }

                r = c.post('/employment_position',
                           data=json.dumps(e_p),
                           headers=self.get_headers())

                return json.loads(r.data)['employment_position']['id']

    def get_employee(self, department_id, position_id,
                     shift_id, user):
        with self.app_context():
            e = EmployeeModel('f_n', 's_n', 'f_sn', 's_sn', '1-11-111',
                              True, date(2000, 1, 31), 'Hombre', 'Panamá',
                              '222-2222', '6666-6666', 'f_n@f_sn.com',
                              'Definido', date(2018, 1, 1),
                              date(2018, 1, 31), date(2018, 1, 15),
                              'Período de Prueba', 104.00, 0, 'ACH', True,
                              1, department_id, position_id, shift_id)
            e.save_to_db()

            return EmployeeModel.find_by_id(e.id, user)

    def get_employee_id(self, e_dict=None):
        with self.app() as c:
            with self.app_context():
                empl = e_dict or {
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
                    'department_id': self.get_department_id(),
                    'position_id': self.get_employment_position_id(),
                    'shift_id': self.get_shift_id()
                }

                r = c.post('/employee',
                           data=json.dumps(empl),
                           headers=self.get_headers())

                return json.loads(r.data)['employee']['id']

    def get_emergency_contact(self, employee_id, organization_id):
        with self.app_context():
            e_c = EmergencyContactModel('f_n', 'l_n', '111-1111', '222-2222',
                                        '6666-6666', employee_id)
            e_c.save_to_db()

            return EmergencyContactModel.find_by_id(e_c.id, organization_id)

    def get_health_permit(self, employee_id, organization_id):
        with self.app_context():
            h_p = HealthPermitModel('Verde', date(2018, 1, 1),
                                    date(2019, 1, 1), employee_id)
            h_p.save_to_db()

            return HealthPermitModel.find_by_id(h_p.id, organization_id)

    def get_passport(self, employee_id, organization_id):
        with self.app_context():
            p = PassportModel('123456', date(2018, 1, 1), date(2019, 1, 1),
                              employee_id, 1)
            p.save_to_db()

            return PassportModel.find_by_id(p.id, organization_id)

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

    def get_bank_account(self, account_number, account_type, is_active,
                         employee_id, bank_id, organization_id):
        with self.app_context():
            b_a = BankAccountModel(account_number, account_type,
                                   is_active, employee_id, bank_id)
            b_a.save_to_db()

            return BankAccountModel.find_by_id(b_a.id, organization_id)

    def get_dependent(self, employee_id, organization_id):
        with self.app_context():
            depen = DependentModel('f_n', 's_n', 'f_sn', 's_sn', 'Mujer',
                                   date(2018, 1, 1), employee_id, 1)
            depen.save_to_db()

            return DependentModel.find_by_id(depen.id, organization_id)

    def get_schedule(self, department_id, organization_id):
        with self.app_context():
            sch = ScheduleModel(date(2018, 1, 1), department_id)

            sch.save_to_db()

            return ScheduleModel.find_by_id(sch.id, organization_id)
