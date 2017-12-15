from unittest import TestCase

from models.organization import OrganizationModel
from models.user import UserModel


class TestOrganization(TestCase):
    """Unit tests for the OrganizationModel."""
    def setUp(self):
        self.o = OrganizationModel('Test Org', True)
        self.u = UserModel('javier', '1234', 1, True, True, True)

    def test_init(self):
        """Test the __init__ method of the OrganizationModel class."""
        self.assertEqual(self.o.name, 'Test Org',
                         f'Wrong name.'
                         f'\nExpected: \'Test Org\''
                         f'\nGot: {self.o.name}')

        self.assertEqual(self.o.is_active, True,
                         f'Wrong is_active.'
                         f'\nExpected: True'
                         f'\nGot: {self.o.is_active}')
