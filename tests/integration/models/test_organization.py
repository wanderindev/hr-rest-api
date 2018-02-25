from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestOrganization(BaseTest):
    """Integration tests for the OrganizationModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up
        a new organization and user.
        """
        super(TestOrganization, self).setUp()

        self.o = self.get_organization()
        self.u = self.get_user(self.o.id)

    def test_find_organization(self):
        """Test the find_by_id method of the OrganizationModel class."""
        with self.app_context():
            print(self.u)
            o = OrganizationModel.find_by_id(self.o.id, self.u)

            self.assertIsNotNone(o)
