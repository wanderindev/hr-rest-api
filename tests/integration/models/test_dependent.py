from models.dependent import DependentModel
from models.employee import EmployeeModel
from tests.base_test import BaseTest


class TestDependent(BaseTest):
    """Integration tests for the DependentModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an employee
        and a dependent.
        """
        super(TestDependent, self).setUp()

        self.e = self.get_employee()
        self.depen = self.get_dependent()

    def test_find_id(self):
        """Test the find_by_id method of DependentModel."""
        with self.app_context():
            depen = DependentModel.find_by_id(self.depen.id, self.u)

            self.assertIsNotNone(depen)

    def test_dependent_list_in_employee(self):
        """ Test that the employee object contains an dependents list. """
        with self.app_context():
            depen_list = DependentModel.query.filter_by(
                employee_id=self.e.id).all()
            depen_list_in_employee = EmployeeModel.find_by_id(
                self.e.id, self.u).dependents

            self.assertListEqual(depen_list, depen_list_in_employee)
