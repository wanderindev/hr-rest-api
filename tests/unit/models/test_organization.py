from unittest import TestCase

from models.organization import OrganizationModel
from models.user import AppUserModel


class TestOrganization(TestCase):
    """Unit tests for the OrganizationModel."""
    def setUp(self):
        self.o = OrganizationModel('test_o', True)
        self.u = AppUserModel('test_u', 'test_p', 'test_u@test_o.com',
                              1, True, True, True)

    def test_init(self):
        """Test the __init__ method of the OrganizationModel class."""
        self.assertEqual(self.o.organization_name, 'test_o')

        self.assertEqual(self.o.is_active, True)
