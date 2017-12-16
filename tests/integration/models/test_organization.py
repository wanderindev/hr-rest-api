from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestOrganization(BaseTest):
    """Integration tests for the OrganizationModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating
        an OrganizationModel object
        """
        super(TestOrganization, self).setUp()
        self.o = OrganizationModel('Test Org', True)

    def test_find_by_name(self):
        """Test the find_by_name methods of the OrganizationModel class."""
        with self.app_context():
            self.o.save_to_db()

            self.assertIsNotNone(OrganizationModel.find_by_name(self.o.name),
                                 f'Did not find organization with name  '
                                 f'{self.o.name} in the db, but expected '
                                 f'to find it.')
