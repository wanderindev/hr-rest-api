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
        Extend the BaseTest setUp method by setting up an organization,
        a department, an employment position, a shift, and an employee.
        """
        super(TestEmployee, self).setUp()

        self.o = self.get_organization()
        self.d = self.get_department(self.o.id)
        self.e_p = self.get_employment_position(self.o.id)
        self.s = self.get_shift(self.o.id)
        self.e = self.get_employee(self.d.id, self.e_p.id, self.s.id, self.o.id)

    def test_find_employee(self):
        """Test the find_by_id method of EmployeeModel."""
        with self.app_context():
            e_id = EmployeeModel.query.filter_by(
                first_name=self.e.first_name).first().id
            e_by_id = EmployeeModel.find_by_id(e_id, self.o.id)

            self.assertIsNotNone(e_by_id)

    def test_employee_list_in_employment_position(self):
        """
        Test that the employment_position object contains an employee list.
        """
        with self.app_context():
            e_list = EmployeeModel.query.filter_by(
                position_id=self.e_p.id).all()
            e_p_e_list = EmploymentPositionModel.find_by_name(
                self.e_p.position_name_feminine, self.o.id).employees

            self.assertListEqual(e_list, e_p_e_list)

    def test_employee_list_in_marital_status(self):
        """Test that the marital_status object contains an employee list."""
        with self.app_context():
            e_list = EmployeeModel.query.filter_by(
                marital_status_id=1).all()
            ms_e_list = MaritalStatusModel.query.filter_by(
                id=1).first().employees

            self.assertListEqual(e_list, ms_e_list)

    def test_employee_list_in_department(self):
        """Test that the department object contains an employee list."""
        with self.app_context():
            e_list = EmployeeModel.query.filter_by(
                department_id=self.d.id).all()
            d_e_list = DepartmentModel.find_by_name(self.d.department_name,
                                                    self.o.id).employees

            self.assertListEqual(e_list, d_e_list)

    def test_employee_list_in_shift(self):
        """Test that the shift object containsan employee list."""
        with self.app_context():
            e_list = EmployeeModel.query.filter_by(
                shift_id=self.s.id).all()
            s_e_list = ShiftModel.find_by_name(self.s.shift_name,
                                               self.o.id).employees

            self.assertListEqual(e_list, s_e_list)
