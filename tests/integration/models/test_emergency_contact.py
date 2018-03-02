from models.emergency_contact import EmergencyContactModel
from models.employee import EmployeeModel
from tests.base_test import BaseTest


class TestEmergencyContact(BaseTest):
    """Integration tests for the EmergencyContactModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an organization, a
        user, a department, an employment position, a shift, an employee,
        and an emergency_contact.
        """
        super(TestEmergencyContact, self).setUp()

        self.o = self.get_organization()
        self.u = self.get_user(self.o.id)
        self.d = self.get_department(self.u)
        self.e_p = self.get_employment_position(self.u)
        self.s = self.get_shift(self.u)
        self.e = self.get_employee(self.d.id, self.e_p.id, self.s.id, self.u)
        self.e_c = self.get_emergency_contact(self.e.id,  self.u)

    def test_find_id(self):
        """Test the find_by_id method of EmergencyContactModel."""
        with self.app_context():
            e_c = EmergencyContactModel.find_by_id(self.e_c.id,
                                                   self.u)

            self.assertIsNotNone(e_c)

    def test_emergency_contact_list_in_employee(self):
        """
        Test that the employee object contains an
        emergency_contacts list.
        """
        with self.app_context():
            e_c_list = EmergencyContactModel.query.filter_by(
                employee_id=self.e.id).all()
            e_c_list_in_employee = EmployeeModel.find_by_id(
                self.e.id, self.u).emergency_contacts

            self.assertListEqual(e_c_list, e_c_list_in_employee)
