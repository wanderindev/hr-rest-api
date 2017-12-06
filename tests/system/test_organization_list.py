import json

from models.organization import OrganizationModel
from models.user import UserModel
from tests.system.base_test import BaseTest


class OrganizationListTest(BaseTest):
    def setUp(self):
        super(OrganizationListTest, self).setUp()
        with self.app_context():
            # Make sure there is one org and a user in db.
            OrganizationModel('TestOrg', True).save_to_db()
            UserModel('javier', '1234', 1, True, True, True).save_to_db()

    def test_org_list_get(self):
        with self.app() as c:
            with self.app_context():
                # Authenticate with registered user.
                r = c.post('/auth', data=json.dumps({
                    'username': 'javier',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})

                # Build and authorization header with access_token returned.
                auth_header = f'JWT {json.loads(r.data)["access_token"]}'

                # Get the organization list from the endpoint.
                r = c.get('/organizations',
                          headers={'Authorization': auth_header})

                # Assert status code for success is returned.
                self.assertEqual(r.status_code, 200,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 200'
                                 f'\nGot: {r.status_code}')

                orgs_dict = {'organizations': [
                    OrganizationModel.find_by_name('TestOrg').json()
                    ]}

                # Assert the endpoint returned the correct organization list.
                self.assertDictEqual(json.loads(r.data),
                                     orgs_dict,
                                     f'\nThe organizations returned by the '
                                     f'endpoint did not meet expectations.'
                                     f'\nExpected: {orgs_dict}'
                                     f'\nGot: {json.loads(r.data)}')

                # Try to get the organization list from the endpoint
                # without authorization.
                r = c.get('/organizations',
                          headers={'Authorization': 'faketoken'})

                # Assert status code for not authorized is returned.
                self.assertEqual(r.status_code, 401,
                                 f'\nWrong status code returned.'
                                 f'\nExpected: 401'
                                 f'\nGot: {r.status_code}')
