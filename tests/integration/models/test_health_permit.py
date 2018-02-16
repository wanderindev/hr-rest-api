from models.health_permit import HealthPermitModel
from models.employee import EmployeeModel
from tests.base_test import BaseTest


class TestHealthPermit(BaseTest):
    """Integration tests for the HealthPermitModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an organization,
        a department, an employment position, a shift, an employee,
        and an health_permit.
        """
        super(TestHealthPermit, self).setUp()

        self.o = self.get_organization()
        self.d = self.get_department(self.o.id)
        self.e_p = self.get_employment_position(self.o.id)
        self.s = self.get_shift(self.o.id)
        self.e = self.get_employee(self.d.id, self.e_p.id, self.s.id, self.o.id)
        self.h_p = self.get_health_permit(self.e.id,  self.o.id)

    def test_find_id(self):
        """Test the find_by_id methods of HealthPermitModel."""
        with self.app_context():
            h_p = HealthPermitModel.find_by_id(self.h_p.id,
                                               self.o.id)

            self.assertIsNotNone(h_p)

    def test_health_permit_list_in_employee(self):
        """
        Test that the employee object contains an
        health_permit list.
        """
        with self.app_context():
            h_p_list = HealthPermitModel.query.filter_by(
                employee_id=self.e.id).all()
            e_h_p_list = EmployeeModel.find_by_id(
                self.e.id, self.o.id).health_permits

            self.assertListEqual(h_p_list, e_h_p_list)
