from datetime import date, time

from models.employee import EmployeeModel
from models.employment_position import EmploymentPositionModel
from models.department import DepartmentModel
from models.marital_status import MaritalStatusModel
from models.shift import ShiftModel
from tests.base_test import BaseTest


class TestEmployee(BaseTest):
    """Integration tests for the EmployeeModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating an EmployeeModel,
        an EmploymentPositionModel, an DepartmentModel and a ShiftModel, and
        saving them to the database before each test.
        """
        super(TestEmployee, self).setUp()

        with self.app_context():
            # Instantiate an employment position, a department and a shift.
            self.e_p = EmploymentPositionModel('test_e_p_f', 'test_e_p_m',
                                               1.00, True, 1)
            self.d = DepartmentModel('test_d', 1, True)
            self.s = ShiftModel('test_s_r', 48, True, 'Quincenal',
                                time(0, 30), False, True, 1,
                                rotation_start_hour=time(6),
                                rotation_end_hour=time(21))

            # Save then to the database.
            self.e_p.save_to_db()
            self.d.save_to_db()
            self.s.save_to_db()

            # Get their ids, so they can be used when instantiating an employee.
            self.e_p_id = EmploymentPositionModel.find_by_name(
                'test_e_p_f', 1).id
            self.d_id = DepartmentModel.find_by_name('test_d', 1).id
            self.s_id = ShiftModel.find_by_name('test_s_r', 1).id

            # Instantiate an employee.
            self.e = EmployeeModel('f_n', 's_n', 'f_sn', 's_sn', '1-11-111',
                                   True, date(2000, 1, 31), 'Hombre', 'Panamá',
                                   '222-2222', '6666-6666', 'f_n@f_sn.com',
                                   'Definido', date(2018, 1, 1),
                                   date(2018, 1, 31), date(2018, 1, 15),
                                   'Período de Prueba', 104.00, 0, 'ACH', True,
                                   1, self.d_id, self.e_p_id, self.s_id)

            # Save employee to database.
            self.e.save_to_db()

    def test_find_employee(self):
        """Test the find_by_id method of EmployeeModel."""
        with self.app_context():
            e_id = EmployeeModel.query.filter_by(first_name='f_n').first().id
            e_by_id = EmployeeModel.find_by_id(e_id, 1)

            self.assertIsNotNone(e_by_id)

    def test_employee_list_in_employment_position(self):
        """
        Test that the employment_position object contains an employee list.
        """
        with self.app_context():
            e_list = EmployeeModel.query.filter_by(
                position_id=self.e_p_id).all()
            e_p_e_list = EmploymentPositionModel.find_by_name(
                'test_e_p_f', 1).employees

            self.assertListEqual(e_list, e_p_e_list)

    def test_employee_list_in_marital_status(self):
        """Test that the marital_status object contains an employee list."""
        with self.app_context():
            e_list = EmployeeModel.query.filter_by(
                position_id=self.e_p_id).all()
            ms_e_list = MaritalStatusModel.query.filter_by(
                id=1).first().employees

            self.assertListEqual(e_list, ms_e_list)

    def test_employee_list_in_department(self):
        """Test that the department object contains an employee list."""
        with self.app_context():
            e_list = EmployeeModel.query.filter_by(
                position_id=self.e_p_id).all()
            d_e_list = DepartmentModel.find_by_name('test_d', 1).employees

            self.assertListEqual(e_list, d_e_list)

    def test_employee_list_in_shift(self):
        """Test that the shift object containsan employee list."""
        with self.app_context():
            e_list = EmployeeModel.query.filter_by(
                position_id=self.e_p_id).all()
            s_e_list = ShiftModel.find_by_name('test_s_r', 1).employees

            self.assertListEqual(e_list, s_e_list)
