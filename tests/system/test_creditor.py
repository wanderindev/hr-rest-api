import json

from models.creditor import CreditorModel
from tests.base_test import BaseTest


class TestCreditor(BaseTest):
    """System tests for the creditor resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a dict
        representing a creditor.
        """
        super(TestCreditor, self).setUp()

        with self.app_context():
            self.cr_dict = {
                'creditor_name': 'test_cr',
                'phone_number': '123-4567',
                'email': 'test@test_cr.com',
                'organization_id': self.get_organization().id,
                'is_active': True
            }

    def test_cred_post_with_authentication(self):
        """
        Test that a POST request to the /creditor endpoint returns
        status code 201 and that the creditor is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                self.assertIsNone(CreditorModel.query.filter_by(
                    creditor_name=self.cr_dict['creditor_name'],
                    organization_id=self.cr_dict['organization_id']).first())

                r = c.post('/creditor',
                           data=json.dumps(self.cr_dict),
                           headers=self.get_headers())

                cred = json.loads(r.data)['creditor']

                self.assertEqual(r.status_code, 201)
                self.assertTrue(cred['is_active'])
                self.assertEqual(cred['creditor_name'],
                                 self.cr_dict['creditor_name'])
                self.assertEqual(cred['phone_number'],
                                 self.cr_dict['phone_number'])
                self.assertEqual(cred['email'],
                                 self.cr_dict['email'])
                self.assertEqual(cred['organization_id'],
                                 self.cr_dict['organization_id'])
                #self.assertListEqual(cred['deductions'], [])
                self.assertIsNotNone(CreditorModel.query.filter_by(
                    creditor_name=self.cr_dict['creditor_name'],
                    organization_id=self.cr_dict['organization_id']).first())

    def test_cred_post_without_authentication(self):
        """
        Test that a POST request to the /creditor endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /creditor endpoint with
                # wrong authentication header.
                r = c.post('/creditor',
                           data=json.dumps(self.cr_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_cred_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicated data to the /creditor endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/creditor',
                       data=json.dumps(self.cr_dict),
                       headers=self.get_headers())

                # Send duplicated POST request.
                r = c.post('/creditor',
                           data=json.dumps(self.cr_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_cred_post_wrong_user(self):
        """
        Test that status code 403 is returned when trying to POST a
        creditor with a user without permission.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/creditor',
                           data=json.dumps(self.cr_dict),
                           headers=self.get_headers({
                               'username': 'test_other_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 403)

    def test_cred_get_with_authentication(self):
        """
        Test that a GET request to the /creditor/<int:creditor_id>
        endpoint returns the correct creditor and status code 200 if the
        user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/creditor/{self.get_creditor().id}',
                          headers=self.get_headers())

                cr = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(cr['creditor_name'],
                                 self.cr_dict['creditor_name'])
                self.assertEqual(cr['phone_number'],
                                 self.cr_dict['phone_number'])
                self.assertEqual(cr['email'],
                                 self.cr_dict['email'])
                self.assertEqual(cr['organization_id'],
                                 self.cr_dict['organization_id'])
                self.assertEqual(cr['is_active'],
                                 self.cr_dict['is_active'])

    def test_cred_get_not_found(self):
        """
        Test that a GET request to the /creditor/<int:creditor_id>
        endpoint returns status code 404 if the creditor is not found in
        the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/creditor/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_cred_get_without_authentication(self):
        """
        Test that a GET request to the /creditor/<int:creditor_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/creditor/{self.get_creditor().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_cred_put_with_authentication(self):
        """
        Test that a PUT request to the /creditor/<int:creditor_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/creditor/{self.get_creditor().id}',
                          data=json.dumps({
                              'creditor_name': 'new_test_cr',
                              'phone_number': '456-7890',
                              'email': 'test@new_test_cr.com',
                              'organization_id': self.cr_dict['organization_id']
                          }),
                          headers=self.get_headers())

                cred = json.loads(r.data)['creditor']

                self.assertTrue(cred['is_active'])
                self.assertEqual(cred['creditor_name'],
                                 'new_test_cr')
                self.assertEqual(cred['phone_number'],
                                 '456-7890')
                self.assertEqual(cred['email'],
                                 'test@new_test_cr.com')
                self.assertEqual(cred['organization_id'],
                                 self.cr_dict['organization_id'])
                self.assertEqual(r.status_code, 200)

    def test_cred_put_without_authentication(self):
        """
        Test that a PUT request to the /creditor/<int:creditor_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/creditor/{self.get_creditor().id}',
                          data=json.dumps({
                              'creditor_name': 'new_test_cr',
                              'phone_number': '456-7890',
                              'email': 'test@new_test_cr.com',
                              'organization_id': self.cr_dict['organization_id']
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_cred_put_not_found(self):
        """
        Test that a PUT request to the /creditor/<int:creditor_id>
        endpoint returns status code 404 if the creditor is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/creditor/1',
                          data=json.dumps({
                              'creditor_name': 'new_test_cr',
                              'phone_number': '456-7890',
                              'email': 'test@new_test_cr.com',
                              'organization_id': self.cr_dict['organization_id']
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_cred_delete_with_authentication(self):
        """
        Test that a DELETE request to the /creditor/<int:creditor_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/creditor/{self.get_creditor().id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_cred_delete_without_authentication(self):
        """
        Test that a DELETE request to the /creditor/<int:creditor_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/creditor/{self.get_creditor().id}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_cred_delete_inactive(self):
        """
        Test that a DELETE request to the /creditor/<int:creditor_id>
        endpoint returns status code 400 if the creditor is already inactive.
        """
        with self.app() as c:
            with self.app_context():
                creditor_id = self.get_creditor().id

                # Make creditor inactive.
                c.delete(f'/creditor/{creditor_id}',
                         headers=self.get_headers())

                # Send DELETE request on inactive creditor.
                r = c.delete(f'/creditor/{creditor_id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_cred_delete_not_found(self):
        """
        Test that a DELETE request to the /creditor/<int:creditor_id>
        endpoint returns status code 404 if the creditor is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/creditor/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_activate_cred_with_authentication(self):
        """
        Test that a PUT request to the /activate_creditor/<int:creditor_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                creditor_id = self.get_creditor().id

                c.delete(f'/creditor/{creditor_id}',
                         headers=self.get_headers())

                r = c.put(f'/activate_creditor/{creditor_id}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_activate_cred_without_authentication(self):
        """
        Test that a PUT request to the /activate_creditor/<int:creditor_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_creditor with
                # wrong authorization header.
                r = c.put(f'/activate_creditor/{self.get_creditor().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_activate_cred_active(self):
        """
        Test that a PUT request to the /activate_creditor/<int:creditor_id>
        endpoint returns status code 400 if the creditor is already active.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_creditor/{self.get_creditor().id}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_activate_cred_not_found(self):
        """
        Test that a PUT request to the /activate_creditor/<int:creditor_id>
        endpoint returns status code 404 if the creditor is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_creditor/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
