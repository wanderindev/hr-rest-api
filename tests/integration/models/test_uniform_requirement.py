from models.employee import EmployeeModel
from models.uniform_requirement import UniformRequirementModel
from tests.base_test import BaseTest


class TestUniformItem(BaseTest):
    """Integration tests for the UniformRequirementModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up all objects
        required to create a uniform requirement.
        """
        super(TestUniformItem, self).setUp()

        with self.app_context():
            self.o = self.get_organization()
            self.d = self.get_department(self.o.id)
            self.e_p = self.get_employment_position(self.o.id)
            self.s = self.get_shift(self.o.id)
            self.e = self.get_employee(self.d.id, self.e_p.id, self.s.id,
                                       self.o.id)
            self.u_i = self.get_uniform_item(self.o.id)
            self.u_s = self.get_uniform_size(self.u_i.id, self.o.id)
            self.u_r = self.get_uniform_requirement(self.e.id, self.u_i.id,
                                                    self.u_s.id, self.o.id)

    def test_find_uniform_requirement(self):
        """Test the find_by_id method of UniformItemModel."""
        with self.app_context():
            u_r_by_id = UniformRequirementModel.find_by_id(self.u_r.id,
                                                           self.o.id)

            self.assertIsNotNone(u_r_by_id)

    def test_uniform_requirement_list_in_employee(self):
        """Test that the employee object contains a uniform requirement list."""
        with self.app_context():
            u_r_list = UniformRequirementModel.query.filter_by(
                employee_id=self.u_r.employee_id).all()
            e_u_r_list = EmployeeModel.find_by_id(
                self.e.id, self.o.id).uniform_requirements

            self.assertListEqual(u_r_list, e_u_r_list)
