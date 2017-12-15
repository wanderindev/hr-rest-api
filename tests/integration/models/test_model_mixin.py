from models.organization import OrganizationModel
from tests.integration.models.base_test import BaseTest


class TestOrganization(BaseTest):
    """Integration tests for the ModelsMixin."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating
        an OrganizationModel object
        """
        super(TestOrganization, self).setUp()
        self.o = OrganizationModel('Test Org', True)

    def test_save_to_db(self):
        """Test the save_to_db method of the ModelsMixin class."""
        with self.app_context():
            self.assertIsNone(OrganizationModel.find_by_name(self.o.name),
                              f'Found organization with name {self.o.name} '
                              f'in the db, but expected not to find it.')

            self.o.save_to_db()

            self.assertIsNotNone(OrganizationModel.find_by_name(self.o.name),
                                 f'Did not find organization with name  '
                                 f'{self.o.name} in the db, but expected '
                                 f'to find it.')

    def test_delete_from_db_exc(self):
        """
        Test that the delete_from_db method of the ModelsMixin class
        raises an exception when trying to delete a record from a table
        that has an is_active column.
        """
        with self.app_context():
            self.o.save_to_db()

            self.assertRaises(ValueError, self.o.delete_from_db)

    def test_activate_inactivate(self):
        """Test the activate and inactivate methods of the ModelsMixin class."""
        with self.app_context():
            self.assertTrue(self.o.is_active,
                            f'The organization is not active but it should be.')

            self.o.inactivate()

            self.assertFalse(self.o.is_active,
                             f'The organization is active but it '
                             f'should not be.')

            self.o.activate()

            self.assertTrue(self.o.is_active,
                            f'The organization is not active but it should be.')
