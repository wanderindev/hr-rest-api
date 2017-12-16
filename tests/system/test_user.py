import json

from models.organization import OrganizationModel
from models.user import UserModel
from tests.base_test import BaseTest


class TestUser(BaseTest):
    """System tests for the organization resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a dict representing
        a user and instantiating an OrganizationModel object and saving it
        to the db so they are available for the different tests.
        """
        super(TestUser, self).setUp()
        with self.app_context():
            self.u_dict = {
                'username': 'javier',
                'password': '1234',
                'organization_id': 1,
                'is_super': True,
                'is_owner': True,
                'is_active': True
            }

            OrganizationModel('Test Org', True).save_to_db()

    def test_user_post_new(self):
        """
        Test that a POST request to the /user endpoint returns
        status code 201 and that the user is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                # Check that the user is not in the db
                # prior to the POST request.
                self.assertIsNone(UserModel.find_by_id(1))

                # Send POST request to /user endpoint.
                r = c.post('/user', data=self.u_dict)

                # Check that status 201 is returned.
                self.assertEqual(r.status_code, 201,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 201'
                                 f'\nGot: {r.status_code}')

                # Check that the user is in the db after the POST request.
                self.assertIsNotNone(UserModel.find_by_id(1),
                                     f'Expected to find user with id 1'
                                     f'in the db but no user was returned.')

    def test_user_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicate data to the /user endpoint.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to /user endpoint.
                c.post('/user', data=self.u_dict)

                # Send duplicated POST request to /user endpoint.
                r = c.post('/user', data=self.u_dict)

                # Check that status code 400 is returned.
                self.assertEqual(r.status_code, 400,
                                 f'Wrong status code returned.'
                                 f'\nExpected: 400'
                                 f'\nGot: {r.status_code}')

    def test_user_get_with_authentication(self):
        """
        Test that a GET request to the /user/<string:username>
        endpoint returns the correct user if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # GET the user from the endpoint.
                r = c.get('/user/javier',
                          headers=self.authorize())

                # Check that status code 200 is returned.
                self.assertEqual(r.status_code, 200,
                                 f'Wrong status code returned.'
                                 f'\nExpected: 200'
                                 f'\nGot: {r.status_code}')

                # Add id=1 to u_dict.
                self.u_dict['id'] = 1

                # Check that the endpoint returned the correct user.
                self.assertDictEqual(json.loads(r.data),
                                     self.u_dict,
                                     f'The user returned by the endpoint'
                                     f'did not meet expectations.'
                                     f'\nExpected: {self.u_dict}'
                                     f'\nGot: {json.loads(r.data)}')

                # Try to get the user from the endpoint without authorization.
                r = c.get('/user/javier',
                          headers={'Authorization': 'faketoken'})

                # Assert status code for not authorized is returned.
                self.assertEqual(r.status_code, 401,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 401'
                                 f'\nGot: {r.status_code}')

    def test_user_get_without_authentication(self):
        """
        Test that a GET request to the /user/<string:username>
        endpoint returns status code 401 if the user is not
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint
                # with wrong access_token.
                r = c.get('/user/javier',
                          headers={'Authorization': 'FaKeToKeN!!'})

                # Check that status code 401 is returned.
                self.assertEqual(r.status_code, 401,
                                 f'Wrong status code returned.'
                                 f'\nExpected: 401'
                                 f'\nGot: {r.status_code}')
