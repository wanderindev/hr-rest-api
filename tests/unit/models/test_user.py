from unittest import TestCase

from models.user import AppUserModel


class TestUser(TestCase):
    """Unit tests for the AppUserModel."""
    def setUp(self):
        self.u = AppUserModel('test_u', 'test_p', 'test_u@test_o.com',
                              1, True, True, True)

    def test_init_and_check_password(self):
        """
        Test the __init__ and check_password methods
        of the AppUserModel class.
        """
        self.assertEqual(self.u.username, 'test_u')
        self.assertTrue(self.u.check_password('test_p'))
        self.assertEqual(self.u.email, 'test_u@test_o.com')
        self.assertEqual(self.u.organization_id, 1)
        self.assertTrue(self.u.is_super)
        self.assertTrue(self.u.is_owner)
        self.assertTrue(self.u.is_active)

    def test_set_password_hash(self):
        """Test the set_password_hash method of the AppUserModel class."""
        self.u.set_password_hash('new_password')
        self.assertTrue(self.u.check_password('new_password'))
