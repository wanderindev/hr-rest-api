from models.organization import OrganizationModel
from models.user import AppUserModel
from tests.base_test import BaseTest


class TestUser(BaseTest):
    """Integration tests for the AppUserModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating
        an OrganizationModel object and a UserModel object
        before each test
        """
        super(TestUser, self).setUp()
        self.o = OrganizationModel('test_o', True)
        self.u = AppUserModel('test_u', 'test_p', 'test_u@test_o.com',
                              1, True, True, True)

    def test_find_user(self):
        """
        Test the find_by_id, find_by_organization_id, and find_by_username
        methods of the AppUserModel class.
        """
        with self.app_context():
            self.o.save_to_db()
            self.u.organization_id = OrganizationModel.find_by_name('test_o').id
            self.u.save_to_db()

            u_by_username = AppUserModel.find_by_username(self.u.username)
            u_by_id = AppUserModel.find_by_id(self.u.id)
            u_by_o_id = AppUserModel.find_by_organization_id(
                self.u.organization_id)[0]

            self.assertIsNotNone(u_by_id)

            self.assertIsNotNone(u_by_username)

            self.assertIsNotNone(u_by_o_id)

            self.assertEqual(u_by_id, u_by_username)

            self.assertEqual(u_by_id, u_by_o_id)

    def test_user_list_in_organization(self):
        """Test that the org object contains a user list."""
        with self.app_context():
            self.o.save_to_db()
            self.u.organization_id = OrganizationModel.find_by_name('test_o').id
            self.u.save_to_db()

            u_list = AppUserModel.find_by_organization_id(self.o.id)
            o_u_list = OrganizationModel.\
                find_by_name(self.o.organization_name).app_users

            self.assertListEqual(u_list, o_u_list)
