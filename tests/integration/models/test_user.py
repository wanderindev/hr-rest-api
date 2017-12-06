from models.organization import OrganizationModel
from models.user import UserModel
from tests.integration.models.base_test import BaseTest


class TestOrganization(BaseTest):
    def setUp(self):
        super(TestOrganization, self).setUp()
        self.org = OrganizationModel('Test Org', True)
        self.u = UserModel('javier', '1234', 1, True, True, True)

    def test_save_and_find(self):
        """
        Test the save_to_db, find_by_id, and find_by_username
        methods of the UserModel class.

        :return: None
        """
        with self.app_context():
            # Assert user is not in db prior to saving.
            self.assertIsNone(UserModel.find_by_username(self.u.username),
                              f'\nFound user with username {self.u.username} '
                              f'in the db, but expected not to find it.')

            # Save org first, since user must belong to an org.
            self.org.save_to_db()
            self.u.save_to_db()

            # Assert user is in db after to saving.
            self.assertIsNotNone(UserModel.find_by_username(self.u.username),
                                 f'\nDid not find user with username  '
                                 f'{self.u.username} in the db, but expected '
                                 f'to find it.')

            # Assert find_by_id and find_by_name return same user.
            self.assertEqual(UserModel.find_by_username(self.u.username),
                             UserModel.find_by_id(self.u.id),
                             f'\nQueries did not return same user.'
                             f'\nBy id: {UserModel.find_by_id(self.u.id)}'
                             f'\nBy username: '
                             f'{UserModel.find_by_username(self.u.username)}')

    def test_delete_from_db(self):
        """
        Test the delete_from_db method of the UserModel class.

        :return: None
        """
        with self.app_context():
            self.org.save_to_db()
            self.u.save_to_db()

            self.u.delete_from_db()

            # Assert user is not in db after delete.
            self.assertIsNone(UserModel.find_by_username(self.u.username),
                              f"\nFound user with username {self.u.username} "
                              f"in the db, but expected not to find it")

    def test_json(self):
        """
        Test the json method of the UserModel class.

        :return: None
        """
        with self.app_context():
            self.org.save_to_db()
            self.u.save_to_db()

            expected_dict = {
                'id': self.u.id,
                'username': self.u.username,
                'password': self.u.password,
                'organization_id': self.u.organization_id,
                'is_super': self.u.is_super,
                'is_owner': self.u.is_owner,
                'is_active': self.u.is_active
            }

            self.assertDictEqual(self.u.json(),
                                 expected_dict,
                                 f'\njson method did not return expected value.'
                                 f'\nExpected: {expected_dict}'
                                 f'\nGot: {self.u.json()}')

    def test_user_list_in_org(self):
        """
        Test that the org object contains a user list

        :return: None
        """
        with self.app_context():
            self.org.save_to_db()
            self.u.save_to_db()

            expected_list = [self.u.json()]

            self.assertListEqual(self.org.json()['users'],
                                 expected_list,
                                 f'\nDid not find the correct user '
                                 f'in the org object.'
                                 f'\nExpected: {expected_list}'
                                 f'\nGot: {self.org.json()["users"]}')
