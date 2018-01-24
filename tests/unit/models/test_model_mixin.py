from unittest import TestCase

from models.user import AppUserModel


class TestModelMixin(TestCase):
    """Unit tests for the ModelMixin class."""
    def setUp(self):
        """Instantiate a UserModel object before each test"""
        self.u = AppUserModel('test_u', 'test_p', 'test_u@test_o.com',
                              1, True, True, True)

    def test_iter(self):
        """Test the __iter__ method of the ModelsMixin class."""
        u_list = [
            ('username', 'test_u'),
            ('password_hash', self.u.password_hash),
            ('email', 'test_u@test_o.com'),
            ('organization_id', 1),
            ('is_super', True),
            ('is_owner', True),
            ('is_active', True)
        ]

        self.assertListEqual(u_list, [*self.u])

        self.assertTrue(self.u.check_password('test_p'))

    def test_repr(self):
        """Test the __repr__ method of the ModelsMixin class."""
        u_repr = "<AppUserModel('username'='test_u', 'password_hash'='" \
                 + self.u.password_hash \
                 + "', 'email'='test_u@test_o.com', 'organization_id'=1, " \
                 + "'is_super'=True, 'is_owner'=True, 'is_active'=True)>"

        self.assertEqual(u_repr, self.u.__repr__())

    def test_to_dict(self):
        """Test the __to_dict__ method of the ModelsMixin class."""
        u_dict = {
            'username': 'test_u',
            'password_hash': self.u.password_hash,
            'email': 'test_u@test_o.com',
            'organization_id': 1,
            'is_super': True,
            'is_owner': True,
            'is_active': True
        }

        self.assertDictEqual(u_dict, self.u.to_dict())
