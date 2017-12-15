from unittest import TestCase

from models.user import UserModel


class TestUser(TestCase):
    """Unit tests for the UserModel."""
    def setUp(self):
        self.u = UserModel('javier', '1234', 1, True, True, True)

    def test_init_and_repr(self):
        """Test the __init__ method of the UserModel class."""
        self.assertEqual(self.u.username, 'javier',
                         f'Wrong username.'
                         f'\nExpected: \'javier\''
                         f'\nGot: {self.u.username}')

        self.assertEqual(self.u.password, '1234',
                         f'Wrong password.'
                         f'\nExpected: \'1234\''
                         f'\nGot: {self.u.password}')

        self.assertEqual(self.u.organization_id, 1,
                         f'Wrong organization_id.'
                         f'\nExpected: 1'
                         f'\nGot: {self.u.organization_id}')

        self.assertEqual(self.u.is_super, True,
                         f'Wrong is_super.'
                         f'\nExpected: True'
                         f'\nGot: {self.u.is_super}')

        self.assertEqual(self.u.is_owner, True,
                         f'Wrong is_owner.'
                         f'\nExpected: True'
                         f'\nGot: {self.u.is_owner}')

        self.assertEqual(self.u.is_active, True,
                         f'Wrong is_active.'
                         f'\nExpected: True'
                         f'\nGot: {self.u.is_active}')
