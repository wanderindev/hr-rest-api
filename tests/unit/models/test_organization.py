from unittest import TestCase

from models.department import DepartmentModel
from models.organization import OrganizationModel
from models.user import AppUserModel


class TestOrganization(TestCase):
    """Unit tests for the OrganizationModel."""

    def test_init(self):
        """Test the __init__ method of the OrganizationModel class."""
        self.o = OrganizationModel('test_o', True)

        self.assertEqual(self.o.organization_name, 'test_o')
        self.assertEqual(self.o.is_active, True)
