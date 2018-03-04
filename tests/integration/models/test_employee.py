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
        Extend the BaseTest setUp method by setting up a department,
        an employment position, a shift, and an employee.
        """
        super(TestEmployee, self).setUp()

        self.d = self.get_department()
        self.e_p = self.get_employment_position()
        self.s = self.get_shift()
        self.e = self.get_employee()

    def test_find_employee(self):
        """Test the find_by_id method of EmployeeModel."""
        with self.app_context():
            e = EmployeeModel.find_by_id(self.e.id, self.u)

            self.assertIsNotNone(e)

    def test_employee_list_in_employment_position(self):
        """
        Test that the employment_position object contains an employee list.
        """
        with self.app_context():
            e_list = EmployeeModel.query.filter_by(
                position_id=self.e_p.id).all()
            e_list_in_emp_pos = EmploymentPositionModel.find_by_id(
                self.e_p.id, self.u).employees

            self.assertListEqual(e_list, e_list_in_emp_pos)

    def test_employee_list_in_marital_status(self):
        """Test that the marital_status object contains an employee list."""
        with self.app_context():
            e_list = EmployeeModel.query.filter_by(
                marital_status_id=1).all()
            e_list_in_mar_status = MaritalStatusModel.query.filter_by(
                id=1).first().employees

            self.assertListEqual(e_list, e_list_in_mar_status)

    def test_employee_list_in_department(self):
        """Test that the department object contains an employee list."""
        with self.app_context():
            e_list = EmployeeModel.query.filter_by(
                department_id=self.d.id).all()
            e_list_in_dept = DepartmentModel.find_by_id(
                self.d.id, self.u).employees

            self.assertListEqual(e_list, e_list_in_dept)

    def test_employee_list_in_shift(self):
        """Test that the shift object contains an employee list."""
        with self.app_context():
            e_list = EmployeeModel.query.filter_by(
                shift_id=self.s.id).all()
            e_list_in_shift = ShiftModel.find_by_id(self.s.id, self.u).employees

            self.assertListEqual(e_list, e_list_in_shift)
