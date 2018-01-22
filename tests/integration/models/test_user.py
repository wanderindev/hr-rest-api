from models.organization import OrganizationModel
from models.user import AppUserModel
from tests.base_test import BaseTest


class TestUser(BaseTest):
    """Integration tests for the UserModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating
        an OrganizationModel object and a UserModel object
        before each test
        """
        super(TestUser, self).setUp()
        self.o = OrganizationModel('Test Org', True)
        self.u = AppUserModel('javier', '1234', 1, True, True, True)

    def test_find_user(self):
        """
        Test the find_by_id, find_by_organization_id, and find_by_username
        methods of the UserModel class.
        """
        with self.app_context():
            self.o.save_to_db()
            self.u.save_to_db()

            u_by_username = AppUserModel.find_by_username(self.u.username)
            u_by_id = AppUserModel.find_by_id(self.u.id)
            u_by_o_id = AppUserModel.find_by_organization_id(
                self.u.organization_id)[0]

            self.assertIsNotNone(u_by_id,
                                 f'The query by id return None, instead of '
                                 f'a user.')

            self.assertIsNotNone(u_by_username,
                                 f'The query by name return None, instead of '
                                 f'a user.')

            self.assertIsNotNone(u_by_o_id,
                                 f'The query by organization_id return None, '
                                 f'instead of a list of user.')

            self.assertEqual(u_by_id, u_by_username,
                             f'The queries did not return the same user.'
                             f'\nBy id: {u_by_id}'
                             f'\nBy username: {u_by_username}')

            self.assertEqual(u_by_id, u_by_o_id,
                             f'The queries did not return the same user.'
                             f'\nBy id: {u_by_id}'
                             f'\nBy organization_id: {u_by_o_id}')

    def test_user_list_in_organization(self):
        """Test that the org object contains a user list."""
        with self.app_context():
            self.o.save_to_db()
            self.u.save_to_db()

            u_list = AppUserModel.find_by_organization_id(self.o.id)
            o_u_list = OrganizationModel.find_by_name(self.o.name).users.all()

            self.assertListEqual(u_list,
                                 o_u_list,
                                 f'Did not find the correct user list '
                                 f'in the org object.'
                                 f'\nExpected: {u_list}'
                                 f'\nGot: {o_u_list}')
