from models.organization import OrganizationModel
from models.user import AppUserModel
from tests.base_test import BaseTest


class TestUser(BaseTest):
    """Integration tests for the AppUserModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating an organization and a
        user, saving them to the database, and getting their ids.
        """
        super(TestUser, self).setUp()

        with self.app_context():
            # Instantiate an organization, save it to the database,
            # and get its id.
            self.o = OrganizationModel('test_o', True)
            self.o.save_to_db()
            self.organization_id = self.o.id

            # Instantiate a user, save it to the database,
            # and get its id.
            self.u = AppUserModel('test_u', 'test_p', 'test_u@test_o.com',
                                  self.organization_id, True, True, True)
            self.u.save_to_db()
            self.user_id = self.u.id
            self.username = self.u.username

    def test_find_user(self):
        """
        Test the find_by_id and find_by_username
        methods of the AppUserModel class.
        """
        with self.app_context():
            u_by_username = AppUserModel.find_by_username(self.username)
            u_by_id = AppUserModel.find_by_id(self.user_id)

            self.assertIsNotNone(u_by_id)
            self.assertIsNotNone(u_by_username)
            self.assertEqual(u_by_id, u_by_username)

    def test_user_list_in_organization(self):
        """Test that the org object contains a user list."""
        with self.app_context():
            u_list = AppUserModel.query.filter_by(
                organization_id=self.organization_id).all()
            o_u_list = OrganizationModel.find_by_id(
                self.organization_id).app_users

            self.assertListEqual(u_list, o_u_list)
