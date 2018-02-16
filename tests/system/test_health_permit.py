import json

from models.health_permit import HealthPermitModel
from tests.base_test import BaseTest


class TestHealthPermit(BaseTest):
    """System tests for the health permit resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a department, an
        employment position, a shift, an employee and a dict representing
        an health permit.
        """
        super(TestHealthPermit, self).setUp()

        with self.app_context():
            self.d = self.get_department(1)
            self.e_p = self.get_employment_position(1)
            self.s = self.get_shift(1)
            self.e = self.get_employee(self.d.id, self.e_p.id, self.s.id, 1)

            self.h_p_dict = {
                'health_permit_type': 'Verde',
                'issue_date': '2018-01-01',
                'expiration_date': '2019-01-01',
                'employee_id': self.e.id
            }

    def test_h_perm_post_with_authentication(self):
        """
        Test that a POST request to the /health_permit endpoint returns
        status code 201 and that the health permit is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/health_permit',
                           data=json.dumps(self.h_p_dict),
                           headers=self.get_headers())

                r_h_perm = json.loads(r.data)['health_permit']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(r_h_perm['health_permit_type'],
                                 self.h_p_dict['health_permit_type'])
                self.assertEqual(r_h_perm['issue_date'],
                                 self.h_p_dict['issue_date'])
                self.assertEqual(r_h_perm['expiration_date'],
                                 self.h_p_dict['expiration_date'])
                self.assertEqual(r_h_perm['employee_id'],
                                 self.h_p_dict['employee_id'])
                self.assertIsNotNone(HealthPermitModel.find_by_id(
                    r_h_perm['id'], 1))

    def test_h_perm_post_without_authentication(self):
        """
        Test that a POST request to the /health_permit endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /health_permit endpoint with
                # wrong authentication header.
                r = c.post('/health_permit',
                           data=json.dumps(self.h_p_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_h_perm_get_with_authentication(self):
        """
        Test that a GET request to the /health_permit/<id:permit_id>
        endpoint returns the correct health permit and status code 200 if
        the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/health_permit',
                           data=json.dumps(self.h_p_dict),
                           headers=self.get_headers())

                permit_id = json.loads(r.data)['health_permit']['id']

                r = c.get(f'/health_permit/{permit_id}',
                          headers=self.get_headers())

                r_dict = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(r_dict['health_permit_type'],
                                 self.h_p_dict['health_permit_type'])
                self.assertEqual(r_dict['issue_date'],
                                 self.h_p_dict['issue_date'])
                self.assertEqual(r_dict['expiration_date'],
                                 self.h_p_dict['expiration_date'])
                self.assertEqual(r_dict['employee_id'],
                                 self.h_p_dict['employee_id'])

    def test_h_perm_get_not_found(self):
        """
        Test that a GET request to the /health_permit/<id:permit_id>
        endpoint returns status code 404 if the health permit is not
        found in the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/health_permit/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_h_perm_get_without_authentication(self):
        """
        Test that a GET request to the /health_permit/<id:permit_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/health_permit/1',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_h_perm_put_with_authentication(self):
        """
        Test that a PUT request to the /health_permit/<id:permit_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/health_permit',
                           data=json.dumps(self.h_p_dict),
                           headers=self.get_headers())

                permit_id = json.loads(r.data)['health_permit']['id']

                r = c.put(f'/health_permit/{permit_id}',
                          data=json.dumps({
                              'health_permit_type': 'Blanco',
                              'issue_date': '2018-01-31',
                              'expiration_date': '2019-01-31',
                              'employee_id': self.e.id
                          }),
                          headers=self.get_headers())

                r_h_perm = json.loads(r.data)['health_permit']

                self.assertEqual(r_h_perm['health_permit_type'],
                                 'Blanco')
                self.assertEqual(r_h_perm['issue_date'],
                                 '2018-01-31')
                self.assertEqual(r_h_perm['expiration_date'],
                                 '2019-01-31')
                self.assertEqual(r_h_perm['employee_id'],
                                 self.e.id)
                self.assertEqual(r.status_code, 200)

    def test_h_perm_put_wrong_employee(self):
        """
        Test that a PUT request to the /health_permit/<id:permit_id>
        endpoint returns status code 500 if the employee_id does not exist.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/health_permit',
                           data=json.dumps(self.h_p_dict),
                           headers=self.get_headers())

                permit_id = json.loads(r.data)['health_permit']['id']

                r = c.put(f'/health_permit/{permit_id}',
                          data=json.dumps({
                              'health_permit_type': 'Verde',
                              'issue_date': '2018-1-31',
                              'expiration_date': '2019-1-31',
                              'employee_id': self.e.id + 1
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 500)

    def test_h_perm_put_without_authentication(self):
        """
        Test that a PUT request to the /health_permit/<id:permit_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/health_permit/1',
                          data=json.dumps({
                              'health_permit_type': 'Verde',
                              'issue_date': '2018-1-31',
                              'expiration_date': '2019-1-31',
                              'employee_id': self.e.id
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_h_perm_put_not_found(self):
        """
        Test that a PUT request to the /health_permit/<id:permit_id>
        endpoint returns status code 404 if the health permit is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/health_permit/1',
                          data=json.dumps({
                              'health_permit_type': 'Verde',
                              'issue_date': '2018-1-31',
                              'expiration_date': '2019-1-31',
                              'employee_id': self.e.id
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_h_perm_delete_with_authentication(self):
        """
        Test that a DELETE request to the /health_permit/<id:permit_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/health_permit',
                           data=json.dumps(self.h_p_dict),
                           headers=self.get_headers())

                permit_id = json.loads(r.data)['health_permit']['id']

                r = c.delete(f'/health_permit/{permit_id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_h_perm_delete_without_authentication(self):
        """
        Test that a DELETE request to the /health_permit/<id:permit_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/health_permit/1',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_h_perm_delete_not_found(self):
        """
        Test that a DELETE request to the /health_permit/<id:permit_id>
        endpoint returns status code 404 if the health permit is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/health_permit/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
