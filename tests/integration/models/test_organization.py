from models.organization import OrganizationModel
from tests.integration.models.base_test import BaseTest


class TestOrganization(BaseTest):
    def setUp(self):
        super(TestOrganization, self).setUp()
        self.org = OrganizationModel('Test Org', True)

    def test_save_and_find(self):
        """
        Test the save_to_db and find_by_name methods of
        the OrganizationModel class.

        :return: None
        """
        with self.app_context():
            # Assert org is not in db prior to saving.
            self.assertIsNone(OrganizationModel.find_by_name(self.org.name),
                              f'\nFound organization with name {self.org.name} '
                              f'in the db, but expected not to find it.')

            self.org.save_to_db()

            # Assert org is in db after to saving.
            self.assertIsNotNone(OrganizationModel.find_by_name(self.org.name),
                                 f'\nDid not find organization with name  '
                                 f'{self.org.name} in the db, but expected '
                                 f'to find it.')

    def test_delete_from_db(self):
        """
        Test the delete_from_db method of the OrganizationModel class.

        :return: None
        """
        with self.app_context():
            self.org.save_to_db()

            self.org.delete_from_db()

            # Assert org is not in db after delete.
            self.assertIsNone(OrganizationModel.find_by_name(self.org.name),
                              f"\nFound organization with name {self.org.name} "
                              f"in the db, but expected not to find it")

    def test_json(self):
        """
        Test the json method of the OrganizationModel class.

        :return: None
        """
        with self.app_context():
            self.org.save_to_db()

            expected_dict = {
                'id': self.org.id,
                'name': self.org.name,
                'is_active': self.org.is_active,
                'users': []
            }

            self.assertDictEqual(self.org.json(),
                                 expected_dict,
                                 f'\njson method did not return expected value.'
                                 f'\nExpected: {expected_dict}'
                                 f'\nGot: {self.org.json()}')
