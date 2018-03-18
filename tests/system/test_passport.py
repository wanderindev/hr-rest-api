import json

from models.passport import PassportModel
from tests.base_test import BaseTest


class TestHealthPermit(BaseTest):
    """System tests for the passport resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a dict 
        representing an passport.
        """
        super(TestHealthPermit, self).setUp()

        with self.app_context():
            self.p_dict = {
                'passport_number': '123456',
                'issue_date': '2018-01-01',
                'expiration_date': '2019-01-01',
                'employee_id': self.get_employee().id,
                'country_id': 1
            }

    def test_passp_post_with_authentication(self):
        """
        Test that a POST request to the /passport endpoint returns
        status code 201 and that the passport is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/passport',
                           data=json.dumps(self.p_dict),
                           headers=self.get_headers())

                passp = json.loads(r.data)['passport']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(passp['passport_number'],
                                 self.p_dict['passport_number'])
                self.assertEqual(passp['issue_date'],
                                 self.p_dict['issue_date'])
                self.assertEqual(passp['expiration_date'],
                                 self.p_dict['expiration_date'])
                self.assertEqual(passp['employee_id'],
                                 self.p_dict['employee_id'])
                self.assertEqual(passp['country_id'],
                                 self.p_dict['country_id'])
                self.assertIsNotNone(PassportModel.find_by_id(
                    passp['id'], self.u))

    def test_passp_post_without_authentication(self):
        """
        Test that a POST request to the /passport endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /passport endpoint with
                # wrong authentication header.
                r = c.post('/passport',
                           data=json.dumps(self.p_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_passp_post_wrong_user(self):
        """
        Test that status code 403 is returned when trying to POST a passport
        with a user without permission.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/passport',
                           data=json.dumps(self.p_dict),
                           headers=self.get_headers({
                               'username': 'test_other_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 403)

    def test_passp_get_with_authentication(self):
        """
        Test that a GET request to the /passport/<id:passport_id>
        endpoint returns the correct passport and status code 200 if
        the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/passport/{self.get_passport().id}',
                          headers=self.get_headers())

                passp = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(passp['passport_number'],
                                 self.p_dict['passport_number'])
                self.assertEqual(passp['issue_date'],
                                 self.p_dict['issue_date'])
                self.assertEqual(passp['expiration_date'],
                                 self.p_dict['expiration_date'])
                self.assertEqual(passp['employee_id'],
                                 self.p_dict['employee_id'])
                self.assertEqual(passp['country_id'],
                                 self.p_dict['country_id'])

    def test_passp_get_not_found(self):
        """
        Test that a GET request to the /passport/<id:passport_id>
        endpoint returns status code 404 if the passport is not
        found in the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/passport/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_passp_get_without_authentication(self):
        """
        Test that a GET request to the /passport/<id:passport_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/passport/{self.get_passport().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_passp_put_with_authentication(self):
        """
        Test that a PUT request to the /passport/<id:passport_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/passport/{self.get_passport().id}',
                          data=json.dumps({
                              'passport_number': '654321',
                              'issue_date': '2018-01-31',
                              'expiration_date': '2019-01-31',
                              'employee_id': self.get_employee().id,
                              'country_id': 2
                          }),
                          headers=self.get_headers())

                passp = json.loads(r.data)['passport']

                self.assertEqual(passp['passport_number'],
                                 '654321')
                self.assertEqual(passp['issue_date'],
                                 '2018-01-31')
                self.assertEqual(passp['expiration_date'],
                                 '2019-01-31')
                self.assertEqual(passp['employee_id'],
                                 self.get_employee().id)
                self.assertEqual(passp['country_id'],
                                 2)
                self.assertEqual(r.status_code, 200)

    def test_passp_put_without_authentication(self):
        """
        Test that a PUT request to the /passport/<id:passport_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/passport/{self.get_passport().id}',
                          data=json.dumps({
                              'passport_number': '654321',
                              'issue_date': '2018-1-31',
                              'expiration_date': '2019-1-31',
                              'employee_id': self.get_employee().id,
                              'country_id': 2
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_passp_put_not_found(self):
        """
        Test that a PUT request to the /passport/<id:passport_id>
        endpoint returns status code 404 if the passport is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/passport/1',
                          data=json.dumps({
                              'passport_number': '654321',
                              'issue_date': '2018-1-31',
                              'expiration_date': '2019-1-31',
                              'employee_id': self.get_employee().id,
                              'country_id': 2
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_passp_delete_with_authentication(self):
        """
        Test that a DELETE request to the /passport/<id:passport_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/passport/{self.get_passport().id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_passp_delete_without_authentication(self):
        """
        Test that a DELETE request to the /passport/<id:passport_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/passport/{self.get_passport().id}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_passp_delete_not_found(self):
        """
        Test that a DELETE request to the /passport/<id:passport_id>
        endpoint returns status code 404 if the passport is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/health_permit/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
