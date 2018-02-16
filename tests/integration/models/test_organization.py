from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestOrganization(BaseTest):
    """Integration tests for the OrganizationModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up
        a new organization.
        """
        super(TestOrganization, self).setUp()

        self.o = self.get_organization()

    def test_find_organization(self):
        """
        Test the find_by_name and find_by_id methods
        of the OrganizationModel class.
        """
        with self.app_context():
            org_by_name = OrganizationModel.find_by_name(
                self.o.organization_name)

            org_by_id = OrganizationModel.find_by_id(self.o.id)

            self.assertIsNotNone(org_by_name)
            self.assertIsNotNone(org_by_id)
            self.assertEqual(org_by_name, org_by_id)
