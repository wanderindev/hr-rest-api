import json

from models.organization import OrganizationModel
from models.user import AppUserModel
from tests.base_test import BaseTest


class TestUser(BaseTest):
    """System tests for the user resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a dict representing
        a user and instantiating an OrganizationModel object and saving it
        to the db so they are available for the different tests.
        """
        super(TestUser, self).setUp()
        with self.app_context():
            OrganizationModel('test_o', True).save_to_db()

            self.u_dict = {
                'username': 'test_u',
                'password': 'test_p',
                'email': 'test_u@test_o.com',
                'organization_id': OrganizationModel.find_by_name('test_o').id,
                'is_super': True,
                'is_owner': True,
                'is_active': True
            }

    def test_user_post_with_authentication(self):
        """
        Test that a POST request to the /user endpoint returns
        status code 201 and that the user is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                # Check that 'test_u' is not in the database.
                self.assertIsNone(AppUserModel.find_by_username('test_u'))

                # Send POST request to the /user endpoint.
                r = c.post('/user',
                           data=json.dumps(self.u_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 201)

                self.assertIsNotNone(AppUserModel.find_by_username('test_u'))

    def test_user_post_without_authentication(self):
        """
        Test that a POST request to the /user endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /user endpoint with
                # wrong authentication header.
                r = c.post('/user',
                           data=json.dumps(self.u_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_user_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicate data to the /user endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/user',
                       data=json.dumps(self.u_dict),
                       headers=self.get_headers())

                # Send duplicated POST request.
                r = c.post('/user',
                           data=json.dumps(self.u_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_user_get_with_authentication(self):
        """
        Test that a GET request to the /user/<string:username>
        endpoint returns the correct user if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/user',
                       data=json.dumps(self.u_dict),
                       headers=self.get_headers())

                # Send GET request to the endpoint.
                r = c.get('/user/test_u',
                          headers=self.get_headers())

                r_dict = json.loads(r.data)

                self.assertEqual(r.status_code, 200)

                self.assertEqual(r_dict['username'],
                                 self.u_dict['username'])

    def test_user_get_not_found(self):
        """
        Test that a GET request to the /user/<string:username>
        endpoint returns status code 404 if the user is not found
        in the database table.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint.
                r = c.get('/user/test_u',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_user_get_without_authentication(self):
        """
        Test that a GET request to the /user/<string:username> endpoint
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the /user endpoint with
                # wrong authentication header.
                r = c.get('/user/test_u',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_user_put_with_authentication(self):
        """
        Test that a PUT request to the /user/<string:username>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/user',
                       data=json.dumps(self.u_dict),
                       headers=self.get_headers())

                # Send PUT request to the /user/test_u endpoint.
                r = c.put('/user/test_u',
                          data=json.dumps({
                              'username': 'new_test_u',
                              'password': 'new_test_p',
                              'email': 'new_test_u@test_o.com',
                              'organization_id': self.u_dict['organization_id'],
                              'is_super': True,
                              'is_owner': True
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_user_put_without_authentication(self):
        """
        Test that a PUT request to the /user/<string:username>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the /user/test_u endpoint with
                # wrong authentication header.
                r = c.put('/user/test_u',
                          data=json.dumps({
                              'username': 'new_test_u',
                              'password': 'new_test_p',
                              'email': 'new_test_u@test_o.com',
                              'organization_id': self.u_dict['organization_id'],
                              'is_super': True,
                              'is_owner': True
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_user_put_not_found(self):
        """
        Test that a PUT request to the /user/<string:username>
        endpoint returns status code 404 if the user is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put('/user/test_u',
                          data=json.dumps({
                              'username': 'new_test_u',
                              'password': 'new_test_p',
                              'email': 'new_test_u@test_o.com',
                              'organization_id': self.u_dict['organization_id'],
                              'is_super': True,
                              'is_owner': True
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_user_delete_with_authentication(self):
        """
        Test that a DELETE request to the /user/<string:username>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/user',
                       data=json.dumps(self.u_dict),
                       headers=self.get_headers())

                # Send DELETE request to the /user/test_u endpoint.
                r = c.delete('/user/test_u',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_user_delete_without_authentication(self):
        """
        Test that a DELETE request to the /user/<string:username>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the /user/test_u endpoint
                # with wrong authorization header.
                r = c.delete('/user/test_u',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_user_delete_inactive(self):
        """
        Test that a DELETE request to the /user/<string:username>
        endpoint returns status code 400 if the user is already inactive.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/user',
                       data=json.dumps(self.u_dict),
                       headers=self.get_headers())

                # Make user inactive.
                c.delete('/user/test_u',
                         headers=self.get_headers())

                # Try DELETE on inactive user.
                r = c.delete('/user/test_u',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_user_delete_not_found(self):
        """
        Test that a DELETE request to the /user/<string:username>
        endpoint returns status code 404 if the user is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete('/user/test_u',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_activate_user_with_authentication(self):
        """
        Test that a PUT request to the /activate_user/<string:username>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/user',
                       data=json.dumps(self.u_dict),
                       headers=self.get_headers())

                # Make user inactive.
                c.delete('/user/test_u',
                         headers=self.get_headers())

                # Send PUT request to /activate_user/test_u
                r = c.put('/activate_user/test_u',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_activate_user_without_authentication(self):
        """
        Test that a PUT request to the /activate_user/<string:username>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_user/test_u with
                # wrong authorization header.
                r = c.put('/activate_user/test_u',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_activate_user_active(self):
        """
        Test that a PUT request to the /activate_user/<string:username>
        endpoint returns status code 400 if the user is already active.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/user',
                       data=json.dumps(self.u_dict),
                       headers=self.get_headers())

                # Send PUT request to /activate_user/test_u
                r = c.put('/activate_user/test_u',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_activate_user_not_found(self):
        """
        Test that a PUT request to the /activate_user/<string:username>
        endpoint returns status code 404 if the user is not found.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_user/test_u
                r = c.put('/activate_user/test_u',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
