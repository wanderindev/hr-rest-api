from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestOrganization(BaseTest):
    """Integration tests for the ModelsMixin."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating
        an OrganizationModel object
        """
        super(TestOrganization, self).setUp()
        self.o = OrganizationModel('test_o', True)

    def test_save_to_db(self):
        """Test the save_to_db method of the ModelsMixin class."""
        with self.app_context():
            self.assertIsNone(OrganizationModel.
                              find_by_name(self.o.organization_name))

            self.o.save_to_db()

            self.assertIsNotNone(OrganizationModel.
                                 find_by_name(self.o.organization_name))

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
            self.assertTrue(self.o.is_active)

            self.o.inactivate()

            self.assertFalse(self.o.is_active)

            self.o.activate()

            self.assertTrue(self.o.is_active)
