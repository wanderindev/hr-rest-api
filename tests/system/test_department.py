import json

from models.department import DepartmentModel
from tests.base_test import BaseTest


class TestDepartment(BaseTest):
    """System tests for the department resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a dict representing
        a department so it is available for the different tests.
        """
        super(TestDepartment, self).setUp()
        with self.app_context():
            self.d_dict = {
                'department_name': 'test_d',
                'organization_id': 1,
                'is_active': True
            }

    def test_dept_post_with_authentication(self):
        """
        Test that a POST request to the /department endpoint returns
        status code 201 and that the department is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                # Check that 'test_d' is not in the database.
                self.assertIsNone(DepartmentModel
                                  .find_by_name('test_d',
                                                self.d_dict['organization_id']))

                # Send POST request to the /department endpoint.
                r = c.post('/department',
                           data=json.dumps(self.d_dict),
                           headers=self.get_headers())

                r_dept = json.loads(r.data)['department']

                self.assertEqual(r.status_code, 201)

                self.assertTrue(r_dept['is_active'])

                self.assertEqual(r_dept['department_name'],
                                 self.d_dict['department_name'])

                self.assertEqual(r_dept['organization_id'],
                                 self.d_dict['organization_id'])

                self.assertListEqual(r_dept['employees'], [])

                self.assertIsNotNone(DepartmentModel
                                     .find_by_name('test_d',
                                                   self.d_dict[
                                                       'organization_id']))

    def test_dept_post_without_authentication(self):
        """
        Test that a POST request to the /department endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /department endpoint with
                # wrong authentication header.
                r = c.post('/department',
                           data=json.dumps(self.d_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_dept_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicate data to the /department endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/department',
                       data=json.dumps(self.d_dict),
                       headers=self.get_headers())

                # Send duplicated POST request.
                r = c.post('/department',
                           data=json.dumps(self.d_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_dept_get_with_authentication(self):
        """
        Test that a GET request to the /department/<string:department_name>
        endpoint returns the correct department if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/department',
                       data=json.dumps(self.d_dict),
                       headers=self.get_headers())

                # Send GET request to the endpoint.
                r = c.get(f'/department/test_d',
                          headers=self.get_headers())

                r_dict = json.loads(r.data)

                self.assertEqual(r.status_code, 200)

                self.assertEqual(r_dict['department_name'],
                                 self.d_dict['department_name'])

    def test_dept_get_not_found(self):
        """
        Test that a GET request to the /department/<string:department_name>
        endpoint returns status code 404 if the department is not found in
        the database table.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint.
                r = c.get(f'/department/test_d',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_dept_get_without_authentication(self):
        """
        Test that a GET request to the /department/<string:department_name>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/department/test_d',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_dept_put_with_authentication(self):
        """
        Test that a PUT request to the /department/<string:department_name>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post(f'/department',
                       data=json.dumps(self.d_dict),
                       headers=self.get_headers())

                # Send PUT request to the endpoint.
                r = c.put(f'/department/test_d',
                          data=json.dumps({
                              'department_name': 'new_test_d',
                              'organization_id': self.d_dict['organization_id'],
                          }),
                          headers=self.get_headers())

                r_dept = json.loads(r.data)['department']

                self.assertTrue(r_dept['is_active'])

                self.assertEqual(r_dept['department_name'],
                                 'new_test_d')

                self.assertEqual(r_dept['organization_id'],
                                 self.d_dict['organization_id'])

                self.assertEqual(r.status_code, 200)

    def test_dept_put_without_authentication(self):
        """
        Test that a PUT request to the /department/<string:department_name
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/department/test_d',
                          data=json.dumps({
                              'department_name': 'new_test_d',
                              'organization_id': self.d_dict['organization_id'],
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_dept_put_not_found(self):
        """
        Test that a PUT request to the /department/<string:department_name
        endpoint returns status code 404 if the department is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/department/test_d',
                          data=json.dumps({
                              'department_name': 'new_test_d',
                              'organization_id': self.d_dict['organization_id'],
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_dept_delete_with_authentication(self):
        """
        Test that a DELETE request to the /department/<string:department_name
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/department',
                       data=json.dumps(self.d_dict),
                       headers=self.get_headers())

                # Send DELETE request to the endpoint.
                r = c.delete(f'/department/test_d',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_dept_delete_without_authentication(self):
        """
        Test that a DELETE request to the /department/<string:department_name
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/department/test_d',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_dept_delete_inactive(self):
        """
        Test that a DELETE request to the /department/<string:department_name
        endpoint returns status code 400 if the department
        is already inactive.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/department',
                       data=json.dumps(self.d_dict),
                       headers=self.get_headers())

                # Make department inactive.
                c.delete(f'/department/test_d',
                         headers=self.get_headers())

                # Try DELETE on inactive department.
                r = c.delete(f'/department/test_d',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_dept_delete_not_found(self):
        """
        Test that a DELETE request to the /department/<string:department_name
        endpoint returns status code 404 if the department is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/department/test_d',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_activate_dept_with_authentication(self):
        """
        Test that a PUT request to the /activate_department
        /<string:department_name endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/department',
                       data=json.dumps(self.d_dict),
                       headers=self.get_headers())

                # Make department inactive.
                c.delete(f'/department/test_d',
                         headers=self.get_headers())

                # Send PUT request to /activate_department
                r = c.put(f'/activate_department/test_d',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_activate_dept_without_authentication(self):
        """
        Test that a PUT request to the /activate_department
        /<string:department_name endpoint returns status code
        401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_department with
                # wrong authorization header.
                r = c.put(f'/activate_department/test_d',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_activate_dept_active(self):
        """
        Test that a PUT request to the /activate_department
        /<string:department_name endpoint returns status code 400
        if the department is already active.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/department',
                       data=json.dumps(self.d_dict),
                       headers=self.get_headers())

                # Send PUT request to /activate_department
                r = c.put(f'/activate_department/test_d',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_activate_dept_not_found(self):
        """
        Test that a PUT request to the /activate_department
        /<string:department_name endpoint returns status code
        404 if the department is not found.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_department
                r = c.put(f'/activate_department/test_d',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
