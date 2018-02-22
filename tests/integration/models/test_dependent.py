from models.dependent import DependentModel
from models.employee import EmployeeModel
from tests.base_test import BaseTest


class TestDependent(BaseTest):
    """Integration tests for the DependentModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an organization,
        a department, an employment position, a shift, an employee,
        and a dependent.
        """
        super(TestDependent, self).setUp()

        self.o = self.get_organization()
        self.d = self.get_department(self.o.id)
        self.e_p = self.get_employment_position(self.o.id)
        self.s = self.get_shift(self.o.id)
        self.e = self.get_employee(self.d.id, self.e_p.id, self.s.id, self.o.id)
        self.depen = self.get_dependent(self.e.id, self.o.id)

    def test_find_id(self):
        """Test the find_by_id methods of DependentModel."""
        with self.app_context():
            depen = DependentModel.find_by_id(self.depen.id,
                                              self.o.id)

            self.assertIsNotNone(depen)

    def test_dependent_list_in_employee(self):
        """
        Test that the employee object contains an
        dependents list.
        """
        with self.app_context():
            depen_list = DependentModel.query.filter_by(
                employee_id=self.e.id).all()
            e_depen_list = EmployeeModel.find_by_id(
                self.e.id, self.o.id).dependents

            self.assertListEqual(depen_list, e_depen_list)
