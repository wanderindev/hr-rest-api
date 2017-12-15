from unittest import TestCase

from models.user import UserModel


class TestModelMixin(TestCase):
    """Unit tests for the ModelMixin class."""
    def setUp(self):
        """Instantiate a UserModel object before each test"""
        self.u = UserModel('javier', '1234', 1, True, True, True)

    def test_iter(self):
        """Test the __iter__ method of the ModelsMixin class."""
        u_list = [
            ('username', 'javier'),
            ('password', '1234'),
            ('organization_id', 1),
            ('is_super', True),
            ('is_owner', True),
            ('is_active', True)
        ]
        self.assertListEqual(u_list, [*self.u],
                             f'The __iter__() method did not return '
                             f'the expected value.'
                             f'\nGot: {[*self.u]}'
                             f'\nExpected: {u_list}')

    def test_repr(self):
        """Test the __repr__ method of the ModelsMixin class."""
        u_repr = "<UserModel('username'='javier', 'password'='1234', " \
                 "'organization_id'=1, 'is_super'=True, 'is_owner'=True, " \
                 "'is_active'=True)>"
        self.assertEqual(u_repr, self.u.__repr__(),
                         f'The __repr__() method did not return '
                         f'the expected string.'
                         f'\nGot: {[self.u.__repr__()]}'
                         f'\nExpected: {u_repr}')

    def test_to_dict(self):
        """Test the __to_dict__ method of the ModelsMixin class."""
        u_dict = {
            'username': 'javier',
            'password': '1234',
            'organization_id': 1,
            'is_super': True,
            'is_owner': True,
            'is_active': True
        }
        self.assertDictEqual(u_dict, self.u.to_dict(),
                             f'The __repr__() method did not return '
                             f'the expected dict.'
                             f'\nGot: {[self.u.to_dict()]}'
                             f'\nExpected: {u_dict}')
