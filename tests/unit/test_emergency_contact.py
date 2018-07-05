from unittest import TestCase

from models.emergency_contact import EmergencyContactModel


class TestEmergencyContact(TestCase):
    """Unit tests for the EmergencyContactModel."""

    def test_init(self):
        """Test the __init__ method of the EmergencyContactModel class."""
        self.e_c = EmergencyContactModel('f_n', 'l_n', '111-1111',
                                         '222-2222', '6666-6666', 1)

        self.assertEqual(self.e_c.first_name, 'f_n')
        self.assertEqual(self.e_c.last_name, 'l_n')
        self.assertEqual(self.e_c.home_phone, '111-1111')
        self.assertEqual(self.e_c.work_phone, '222-2222')
        self.assertEqual(self.e_c.mobile_phone, '6666-6666')
        self.assertEqual(self.e_c.employee_id, 1)
