import json

from models.organization import OrganizationModel
from tests.system.base_test import BaseTest


class OrganizationTest(BaseTest):
    def test_org_post_new(self):
        with self.app() as c:
            with self.app_context():
                org_dict = {'name': 'TestOrg', 'is_active': True}

                # Assert 'TestOrg' is not in db.
                self.assertIsNone(OrganizationModel.find_by_name('TestOrg'))

                # Register the organization.
                r = c.post('/organization', data=org_dict)

                # Assert status code for created is returned.
                self.assertEqual(r.status_code, 201,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 201'
                                 f'\nGot: {r.status_code}')

                # Assert user with id 1 is in db.
                self.assertIsNotNone(OrganizationModel.find_by_name('TestOrg'),
                                     f'Expected to find organization with name'
                                     f'"Test Org" in the db but no organization'
                                     f' was returned.')

    def test_org_post_duplicate(self):
        with self.app() as c:
            with self.app_context():
                org_dict = {'name': 'TestOrg', 'is_active': True}

                # Assert 'TestOrg' is not in db.
                self.assertIsNone(OrganizationModel.find_by_name('TestOrg'))

                # Register the organization.
                c.post('/organization', data=org_dict)

                # Register same organization again.
                r = c.post('/organization', data=org_dict)

                # Assert status code for bad request is returned.
                self.assertEqual(r.status_code, 400,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 400'
                                 f'\nGot: {r.status_code}')

    def test_org_get(self):
        with self.app() as c:
            with self.app_context():
                org_dict = {'name': 'TestOrg', 'is_active': True}

                user_dict = {
                    'username': 'javier',
                    'password': '1234',
                    'organization_id': 1,
                    'is_super': True,
                    'is_owner': True,
                    'is_active': True
                }

                # Register the organization.
                c.post('/organization', data=org_dict)

                # Register the user.
                c.post('/user', data=user_dict)

                # Authenticate with registered user.
                r = c.post('/auth', data=json.dumps({
                    'username': 'javier',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})

                # Build and authorization header with access_token returned.
                auth_header = f'JWT {json.loads(r.data)["access_token"]}'

                # Get the organization from the endpoint.
                r = c.get('/organization/TestOrg',
                          headers={'Authorization': auth_header})

                # Assert status code for success is returned.
                self.assertEqual(r.status_code, 200,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 200'
                                 f'\nGot: {r.status_code}')

                # Add the id to org_dict and user_dict.
                org_dict['id'] = 1
                user_dict['id'] = 1

                # Add the user to org_dict.
                org_dict['users'] = [user_dict]

                # Assert the endpoint returned the correct organization.
                self.assertDictEqual(json.loads(r.data),
                                     org_dict,
                                     f'\nThe organization returned by the '
                                     f'endpoint did not meet expectations.'
                                     f'\nExpected: {org_dict}'
                                     f'\nGot: {json.loads(r.data)}')

                # Try to get the organization from the endpoint
                # without authorization.
                r = c.get('/organization/TestOrg',
                          headers={'Authorization': 'faketoken'})

                # Assert status code for not authorized is returned.
                self.assertEqual(r.status_code, 401,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 401'
                                 f'\nGot: {r.status_code}')
