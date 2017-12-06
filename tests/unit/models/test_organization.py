from unittest import TestCase

from models.organization import OrganizationModel
# noinspection PyUnresolvedReferences
from models.user import UserModel


class TestOrganization(TestCase):
    def setUp(self):
        self.org = OrganizationModel('Test Org', True)

    def test_init_and_repr(self):
        """
        Test the __init__ and __repr__ methods of
        the OrganizationModel class.

        :return: None
        """
        org_str = f'<OrganizationModel(name={self.org.name!r}, ' \
                  f'is_active={self.org.is_active!r})>'

        self.assertEqual(str(self.org),
                         org_str,
                         f'\nWrong organization __repr__.'
                         f'\nExpected: {org_str}'
                         f'\nGot: {str(self.org)}')
