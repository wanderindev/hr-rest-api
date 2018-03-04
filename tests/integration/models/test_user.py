from models.organization import OrganizationModel
from models.user import AppUserModel
from tests.base_test import BaseTest


class TestUser(BaseTest):
    """Integration tests for the AppUserModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up
        an organization.
        """
        super(TestUser, self).setUp()

        self.o = self.get_organization()

    def test_find_user(self):
        """
        Test the find_by_id and find_by_username
        methods of the AppUserModel class.
        """
        with self.app_context():
            u_by_username = AppUserModel.find_by_username(self.u.username)
            u_by_id = AppUserModel.find_by_id(self.u.id)

            self.assertIsNotNone(u_by_id)
            self.assertIsNotNone(u_by_username)
            self.assertEqual(u_by_id, u_by_username)

    def test_user_list_in_organization(self):
        """Test that the org object contains a user list."""
        with self.app_context():
            u_list = AppUserModel.query.filter_by(
                organization_id=self.o.id).all()
            o_u_list = OrganizationModel.query.filter_by(
                id=self.o.id).first().app_users

            self.assertListEqual(u_list, o_u_list)
