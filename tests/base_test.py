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
            EmployeeModel.query.delete()
            EmploymentPositionModel.query.delete()
            ShiftModel.query.delete()
            UniformSizeModel.query.delete()
            UniformItemModel.query.delete()
            DepartmentModel.query.delete()
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

    def get_organization(self):
        with self.app_context():
            o = OrganizationModel('test_o', True)
            o.save_to_db()

            return OrganizationModel.find_by_id(o.id)

    def get_user(self, organization_id):
        with self.app_context():
            u = AppUserModel('test_u', 'test_p', 'test_u@test_o.com',
                             organization_id, True, True, True)
            u.save_to_db()

            return AppUserModel.find_by_id(u.id)

    def get_department(self, organization_id):
        with self.app_context():
            d = DepartmentModel('test_d', organization_id, True)
            d.save_to_db()

            return DepartmentModel.find_by_id(d.id, organization_id)

    def get_shift(self, organization_id):
        with self.app_context():
            s = ShiftModel('test_s_r', 48, True, 'Quincenal',
                           time(0, 30), False, True, organization_id,
                           rotation_start_hour=time(6),
                           rotation_end_hour=time(21))
            s.save_to_db()

            return ShiftModel.find_by_id(s.id, organization_id)

    def get_employment_position(self, organization_id):
        with self.app_context():
            e_p = EmploymentPositionModel('test_e_p_f', 'test_e_p_m',
                                          1.00, True, organization_id)
            e_p.save_to_db()

            return EmploymentPositionModel.find_by_id(e_p.id, organization_id)

    def get_employee(self, department_id, position_id,
                     shift_id, organization_id):
        with self.app_context():
            e = EmployeeModel('f_n', 's_n', 'f_sn', 's_sn', '1-11-111',
                              True, date(2000, 1, 31), 'Hombre', 'Panamá',
                              '222-2222', '6666-6666', 'f_n@f_sn.com',
                              'Definido', date(2018, 1, 1),
                              date(2018, 1, 31), date(2018, 1, 15),
                              'Período de Prueba', 104.00, 0, 'ACH', True,
                              1, department_id, position_id, shift_id)
            e.save_to_db()

            return EmployeeModel.find_by_id(e.id, organization_id)

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
