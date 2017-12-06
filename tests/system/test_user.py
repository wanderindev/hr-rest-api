import json

from models.organization import OrganizationModel
from models.user import UserModel
from tests.system.base_test import BaseTest


class UserTest(BaseTest):
    def setUp(self):
        super(UserTest, self).setUp()
        with self.app_context():
            # Make sure there is one org in db.
            OrganizationModel('TestOrg', True).save_to_db()

    def test_user_post_new(self):
        with self.app() as c:
            with self.app_context():
                user_dict = {
                    'username': 'javier',
                    'password': '1234',
                    'organization_id': 1,
                    'is_super': True,
                    'is_owner': True,
                    'is_active': True
                }

                # Assert user with id 1 is not in db.
                self.assertIsNone(UserModel.find_by_id(1))

                # Register a user.
                r = c.post('/user', data=user_dict)

                # Assert status code for created is returned.
                self.assertEqual(r.status_code, 201,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 201'
                                 f'\nGot: {r.status_code}')

                # Assert user with id 1 is in db.
                self.assertIsNotNone(UserModel.find_by_id(1),
                                     f'Expected to find user with id 1'
                                     f'in the db but no user was returned.')

    def test_user_post_duplicate(self):
        with self.app() as c:
            with self.app_context():
                user_dict = {
                    'username': 'javier',
                    'password': '1234',
                    'organization_id': 1,
                    'is_super': True,
                    'is_owner': True,
                    'is_active': True
                }

                # Assert user with id 1 is not in db.
                self.assertIsNone(UserModel.find_by_id(1))

                # Register a user.
                c.post('/user', data=user_dict)

                # Register same user again.
                r = c.post('/user', data=user_dict)

                # Assert status code for bad request is returned.
                self.assertEqual(r.status_code, 400,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 400'
                                 f'\nGot: {r.status_code}')

    def test_user_get(self):
        with self.app() as c:
            with self.app_context():
                user_dict = {
                    'username': 'javier',
                    'password': '1234',
                    'organization_id': 1,
                    'is_super': True,
                    'is_owner': True,
                    'is_active': True
                }

                # Register a user.
                c.post('/user', data=user_dict)

                # Authenticate with registered user.
                r = c.post('/auth', data=json.dumps({
                    'username': 'javier',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})

                # Build and authorization header with access_token returned.
                auth_header = f'JWT {json.loads(r.data)["access_token"]}'

                # Get the user from the endpoint.
                r = c.get('/user/javier',
                          headers={'Authorization': auth_header})

                # Assert status code for success is returned.
                self.assertEqual(r.status_code, 200,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 200'
                                 f'\nGot: {r.status_code}')

                # Add the id to user_dict.
                user_dict['id'] = 1

                # Assert the endpoint returned the correct user.
                self.assertDictEqual(json.loads(r.data),
                                     user_dict,
                                     f'\nThe user returned by the endpoint'
                                     f'did not meet expectations.'
                                     f'\nExpected: {user_dict}'
                                     f'\nGot: {json.loads(r.data)}')

                # Try to get the user from the endpoint without authorization.
                r = c.get('/user/javier',
                          headers={'Authorization': 'faketoken'})

                # Assert status code for not authorized is returned.
                self.assertEqual(r.status_code, 401,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 401'
                                 f'\nGot: {r.status_code}')
