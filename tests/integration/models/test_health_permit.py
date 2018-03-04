from models.health_permit import HealthPermitModel
from models.employee import EmployeeModel
from tests.base_test import BaseTest


class TestHealthPermit(BaseTest):
    """Integration tests for the HealthPermitModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an employee
        and an health_permit.
        """
        super(TestHealthPermit, self).setUp()

        self.e = self.get_employee()
        self.h_p = self.get_health_permit()

    def test_find_id(self):
        """Test the find_by_id method of HealthPermitModel."""
        with self.app_context():
            h_p = HealthPermitModel.find_by_id(self.h_p.id,
                                               self.u)

            self.assertIsNotNone(h_p)

    def test_health_permit_list_in_employee(self):
        """
        Test that the employee object contains an
        health_permit list.
        """
        with self.app_context():
            h_p_list = HealthPermitModel.query.filter_by(
                employee_id=self.e.id).all()
            h_p_list_in_employee = EmployeeModel.find_by_id(
                self.e.id, self.u).health_permits

            self.assertListEqual(h_p_list, h_p_list_in_employee)
