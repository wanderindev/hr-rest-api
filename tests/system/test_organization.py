import json

from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestOrganization(BaseTest):
    """System tests for the organization resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating dicts
        representing a user and an organization so they are
        available for the different tests.
        """
        super(TestOrganization, self).setUp()
        self.o_dict = {
            'name': 'Test Org',
            'is_active': True
        }

        self.u_dict = {
            'username': 'javier',
            'password': '1234',
            'organization_id': 1,
            'is_super': True,
            'is_owner': True,
            'is_active': True
        }

    def test_organization_post_new(self):
        """
        Test that a POST request to the /organization endpoint returns
        status code 201 and that the organization is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                # Check that 'Test Org' is not in the db to begin with.
                self.assertIsNone(OrganizationModel.find_by_name('Test Org'))

                # Send POST request to the /organization endpoint.
                r = c.post('/organization', data=self.o_dict)

                # Check that status code 201 is returned.
                self.assertEqual(r.status_code, 201,
                                 f'Wrong status code returned.'
                                 f'\nExpected: 201'
                                 f'\nGot: {r.status_code}')

    def test_organization_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicate data to the /organization endpoint.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /organization endpoint.
                c.post('/organization', data=self.o_dict)

                # Send duplicated POST request to the /organization endpoint.
                r = c.post('/organization', data=self.o_dict)

                # Check that status code 400 is returned.
                self.assertEqual(r.status_code, 400,
                                 f'Wrong status code returned.'
                                 f'\nExpected: 400'
                                 f'\nGot: {r.status_code}')

    def test_organization_get_with_authentication(self):
        """
        Test that a GET request to the /organization/<string:name>
        endpoint returns the correct organization if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Register the organization.
                c.post('/organization', data=self.o_dict)

                # Send the GET request to the endpoint.
                r = c.get('/organization/Test%20Org',
                          headers=self.authorize())

                # Check that status code 200 is returned.
                self.assertEqual(r.status_code, 200,
                                 f'Wrong status code returned.'
                                 f'\nExpected: 200'
                                 f'\nGot: {r.status_code}')

                # Add the id=1 to o_dict.
                self.o_dict['id'] = 1

                # Check that the endpoint returned the
                # correct organization.
                self.assertDictEqual(json.loads(r.data),
                                     self.o_dict,
                                     f'\The organization returned by the '
                                     f'endpoint did not meet expectations.'
                                     f'\nExpected: {self.o_dict}'
                                     f'\nGot: {json.loads(r.data)}')

    def test_organization_get_without_authentication(self):
        """
        Test that a GET request to the /organization/<string:name>
        endpoint returns status code 401 if the user is not
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Register the organization.
                c.post('/organization', data=self.o_dict)

                # Send the GET request to the endpoint
                # with wrong access_token.
                r = c.get('/organization/Test%20Org',
                          headers={'Authorization': 'FaKeToKeN!!'})

                # Check that status code 401 is returned.
                self.assertEqual(r.status_code, 401,
                                 f'Wrong status code returned.'
                                 f'\nExpected: 401'
                                 f'\nGot: {r.status_code}')

    def test_organization_list_with_authentication(self):
        """
        Test that GET requests to the /organizations endpoint
        returns the list of organizations if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Register the organization.
                c.post('/organization', data=self.o_dict)

                # Get the organization list from the endpoint.
                r = c.get('/organizations',
                          headers=self.authorize())

                # Check that status code 200 is returned.
                self.assertEqual(r.status_code, 200,
                                 f'Wrong status code returned.'
                                 f'\nExpected: 200'
                                 f'\nGot: {r.status_code}')

                expected = {
                    'organizations': [
                        OrganizationModel.find_by_name('Test Org').to_dict()
                    ]
                }

                # Check that the endpoint returned the correct organizations.
                self.assertDictEqual(json.loads(r.data),
                                     expected,
                                     f'The organizations returned by the '
                                     f'endpoint did not meet expectations.'
                                     f'\nExpected: {expected}'
                                     f'\nGot: {json.loads(r.data)}')

    def test_organization_list_without_authentication(self):
        """
        Test that GET requests to the /organizations endpoint
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Register the organization.
                c.post('/organization', data=self.o_dict)

                # Send the GET request to the endpoint
                # with wrong access_token.
                r = c.get('/organizations',
                          headers={'Authorization': 'FaKeToKeN!!'})

                # Check that status code 401 is returned.
                self.assertEqual(r.status_code, 401,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 401'
                                 f'\nGot: {r.status_code}')