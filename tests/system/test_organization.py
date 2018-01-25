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
            'organization_name': 'test_o',
            'is_active': True
        }

        self.u_dict = {
            'username': 'test_u',
            'password': 'test_p',
            'email': 'test_u@test_o.com',
            'organization_id': 1,
            'is_super': True,
            'is_owner': True,
            'is_active': True
        }

    def test_organization_post_with_authentication(self):
        """
        Test that a POST request to the /organization endpoint returns
        status code 201 and that the organization is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                # Check that 'test_o' is not in the database.
                self.assertIsNone(OrganizationModel.find_by_name('test_o'))

                # Send POST request to the /organization endpoint.
                r = c.post('/organization',
                           data=json.dumps(self.o_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 201)

                self.assertIsNotNone(OrganizationModel.find_by_name('test_o'))

    def test_organization_post_without_authentication(self):
        """
        Test that a POST request to the /organization
        endpoint returns status code 401 if the user is not
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /organization endpoint with
                # wrong authentication header.
                r = c.post('/organization',
                           data=json.dumps(self.o_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_organization_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicate data to the /organization endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/organization',
                       data=json.dumps(self.o_dict),
                       headers=self.get_headers())

                # Send duplicated POST request.
                r = c.post('/organization',
                           data=json.dumps(self.o_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_organization_get_with_authentication(self):
        """
        Test that a GET request to the /organization/<string:organization_name>
        endpoint returns the correct organization if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/organization',
                       data=json.dumps(self.o_dict),
                       headers=self.get_headers())

                # Send GET request to the endpoint.
                r = c.get('/organization/test_o',
                          headers=self.get_headers())

                r_dict = json.loads(r.data)

                self.assertEqual(r.status_code, 200)

                self.assertEqual(r_dict['organization_name'],
                                 self.o_dict['organization_name'])

    def test_organization_get_not_found(self):
        """
        Test that a GET request to the /organization/<string:organization_name>
        endpoint returns status code 404 if the organization is not found
        in the database table.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint.
                r = c.get('/organization/test_o',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_organization_get_without_authentication(self):
        """
        Test that a GET request to the /organization/<string:organization_name>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the /organization endpoint with
                # wrong authentication header.
                r = c.get('/organization/Test%20Org',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_organization_put_with_authentication(self):
        """
        Test that a PUT request to the /organization/<string:organization_name>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/organization',
                       data=json.dumps(self.o_dict),
                       headers=self.get_headers())

                # Send PUT request to the /organization/test_o endpoint.
                r = c.put('/organization/test_o',
                          data=json.dumps({
                              'organization_name': 'new_test_o'
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_organization_put_without_authentication(self):
        """
        Test that a PUT request to the /organization/<string:organization_name>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the /organization/
                # <string:organization_name>  endpoint.
                r = c.put('/organization/test_o',
                          data=json.dumps({
                              'organization_name': 'new_test_o'
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                # Check that status code 401 is returned.
                self.assertEqual(r.status_code, 401)

    def test_organization_put_not_found(self):
        """
        Test that a PUT request to the /organization/<string:organization_name>
        endpoint returns status code 404 if the organization is not in the
        database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put('/organization/test_o',
                          data=json.dumps({
                              'organization_name': 'new_test_o'
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_organization_delete_with_authentication(self):
        """
        Test that a DELETE request to the
        /organization/<string:organization_name>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/organization',
                       data=json.dumps(self.o_dict),
                       headers=self.get_headers())

                # Send DELETE request to the /organization/test_o endpoint.
                r = c.delete('/organization/test_o',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_organization_delete_without_authentication(self):
        """
        Test that a DELETE request to the
        /organization/<string:organization_name>
        endpoint returns status code 401 if user
        is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the /organization/test_o endpoint
                # with wrong authorization header.
                r = c.delete('/organization/test_o',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_organization_delete_inactive(self):
        """
        Test that a DELETE request to the
        /organization/<string:organization_name>
        endpoint returns status code 400 if the
        organization is already inactive.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/organization',
                       data=json.dumps(self.o_dict),
                       headers=self.get_headers())

                # Make organization inactive.
                c.delete('/organization/test_o',
                         headers=self.get_headers())

                # Try DELETE on inactive organization.
                r = c.delete('/organization/test_o',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_organization_delete_not_found(self):
        """
        Test that a DELETE request to the
        /organization/<string:organization_name>
        endpoint returns status code 404 if the
        organization is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete('/organization/test_o',
                             headers=self.get_headers())

                # Check that status code 404 is returned.
                self.assertEqual(r.status_code, 404)

    def test_activate_organization_with_authentication(self):
        """
        Test that a PUT request to the
        /activate_organization/<string:organization_name>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/organization',
                       data=json.dumps(self.o_dict),
                       headers=self.get_headers())

                # Make organization inactive.
                c.delete('/organization/test_o',
                         headers=self.get_headers())

                # Send PUT request to /activate_organization/test_o
                r = c.put('/activate_organization/test_o',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_activate_organization_without_authentication(self):
        """
        Test that a PUT request to the
        /activate_organization/<string:organization_name>
        endpoint returns status code 401 if user
        is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_organization with
                # wrong authorization header.
                r = c.put('/activate_organization/test_o',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_activate_organization_active(self):
        """
        Test that a PUT request to the
        /activate_organization/<string:organization_name>
        endpoint returns status code 400 if the
        organization is already active.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/organization',
                       data=json.dumps(self.o_dict),
                       headers=self.get_headers())

                # Send PUT request to /activate_organization
                r = c.put('/activate_organization/test_o',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_activate_organization_not_found(self):
        """
        Test that a PUT request to the
        /activate_organization/<string:organization_name>
        endpoint returns status code 404 if the
        organization was not found.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_organization
                r = c.put('/activate_organization/test_o',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_organization_list_with_authentication(self):
        """
        Test that GET requests to the /organizations endpoint
        returns the list of organizations if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/organization',
                       data=json.dumps(self.o_dict),
                       headers=self.get_headers())

                # Get the organization list from the endpoint.
                r = c.get('/organizations',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

                expected = {
                    'organizations': [
                        OrganizationModel.find_by_name('Nuvanz').to_dict(),
                        OrganizationModel.find_by_name('test_o').to_dict()
                    ]
                }

                self.assertDictEqual(json.loads(r.data), expected)

    def test_organization_list_without_authentication(self):
        """
        Test that GET requests to the /organizations endpoint
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint
                # with wrong authorization header.
                r = c.get('/organizations',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)
