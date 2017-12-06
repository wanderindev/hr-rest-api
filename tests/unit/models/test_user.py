from unittest import TestCase

from models.user import UserModel


class TestUser(TestCase):
    def setUp(self):
        self.u = UserModel('javier', '1234', 1, True, True, True)

    def test_init_and_repr(self):
        """
        Test the __init__ and __repr__ methods of
        the UserModel class.

        :return: None
        """
        u_str = f'<UserModel(username={self.u.username!r}, ' \
                f'password={self.u.password!r}, ' \
                f'organization_id={self.u.organization_id!r}, ' \
                f'is_super={self.u.is_super!r}, ' \
                f'is_owner={self.u.is_owner!r}, ' \
                f'is_active={self.u.is_active!r})>'

        self.assertEqual(str(self.u),
                         u_str,
                         f'\nWrong organization __repr__.'
                         f'\nExpected: {u_str}'
                         f'\nGot: {str(self.u)}')
