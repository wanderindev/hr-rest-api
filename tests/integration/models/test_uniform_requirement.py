from models.employee import EmployeeModel
from models.uniform_requirement import UniformRequirementModel
from tests.base_test import BaseTest


class TestUniformItem(BaseTest):
    """Integration tests for the UniformRequirementModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an employee and
        a uniform requirement object.
        """
        super(TestUniformItem, self).setUp()

        with self.app_context():
            self.e = self.get_employee()
            self.u_r = self.get_uniform_requirement()

    def test_find_uniform_requirement(self):
        """Test the find_by_id method of UniformItemModel."""
        with self.app_context():
            u_r = UniformRequirementModel.find_by_id(self.u_r.id, self.u)

            self.assertIsNotNone(u_r)

    def test_uniform_requirement_list_in_employee(self):
        """Test that the employee object contains a uniform requirement list."""
        with self.app_context():
            u_r_list = UniformRequirementModel.query.filter_by(
                employee_id=self.u_r.employee_id).all()
            u_r_list_in_emp = EmployeeModel.find_by_id(
                self.e.id, self.u).uniform_requirements

            self.assertListEqual(u_r_list, u_r_list_in_emp)
