import json

from models.department import DepartmentModel
from tests.base_test import BaseTest


class TestDepartment(BaseTest):
    """System tests for the department resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating an organization,
        a user, and dict representing a department so it is available
        for the different tests.
        """
        super(TestDepartment, self).setUp()

        with self.app_context():
            self.o = self.get_organization()
            self.u = self.get_user(self.o.id, False)

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
                self.assertIsNone(DepartmentModel.query.filter_by(
                    department_name=self.d_dict['department_name'],
                    organization_id=self.d_dict['organization_id']).first())

                r = c.post('/department',
                           data=json.dumps(self.d_dict),
                           headers=self.get_headers())

                dept = json.loads(r.data)['department']

                self.assertEqual(r.status_code, 201)
                self.assertTrue(dept['is_active'])
                self.assertEqual(dept['department_name'],
                                 self.d_dict['department_name'])
                self.assertEqual(dept['organization_id'],
                                 self.d_dict['organization_id'])
                self.assertListEqual(dept['employees'], [])
                self.assertIsNotNone(DepartmentModel.query.filter_by(
                    department_name=self.d_dict['department_name'],
                    organization_id=self.d_dict['organization_id']).first())

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
        POST duplicated data to the /department endpoint.
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

    def test_dept_post_wrong_organization(self):
        """
        Test that status code 401 is returned when trying to POST a
        department that does not belong to the user's organization.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/department',
                           data=json.dumps(self.d_dict),
                           headers=self.get_headers({
                               'username': 'test_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 401)

    def test_dept_get_with_authentication(self):
        """
        Test that a GET request to the /department/<int:department_id>
        endpoint returns the correct department and status code 200 if the
        user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/department/{self.get_department_id()}',
                          headers=self.get_headers())

                d = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(d['department_name'],
                                 self.d_dict['department_name'])
                self.assertEqual(d['organization_id'],
                                 self.d_dict['organization_id'])
                self.assertEqual(d['is_active'],
                                 self.d_dict['is_active'])

    def test_dept_get_not_found(self):
        """
        Test that a GET request to the /department/<int:department_id>
        endpoint returns status code 404 if the department is not found in
        the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/department/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_dept_get_without_authentication(self):
        """
        Test that a GET request to the /department/<int:department_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/department/{self.get_department_id()}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_dept_put_with_authentication(self):
        """
        Test that a PUT request to the /department/<int:department_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/department/{self.get_department_id()}',
                          data=json.dumps({
                              'department_name': 'new_test_d',
                              'organization_id': self.d_dict['organization_id']
                          }),
                          headers=self.get_headers())

                dept = json.loads(r.data)['department']

                self.assertTrue(dept['is_active'])
                self.assertEqual(dept['department_name'],
                                 'new_test_d')
                self.assertEqual(dept['organization_id'],
                                 self.d_dict['organization_id'])
                self.assertEqual(r.status_code, 200)

    def test_dept_put_without_authentication(self):
        """
        Test that a PUT request to the /department/<int:department_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/department/{self.get_department_id()}',
                          data=json.dumps({
                              'department_name': 'new_test_d',
                              'organization_id': self.d_dict['organization_id']
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_dept_put_not_found(self):
        """
        Test that a PUT request to the /department/<int:department_id>
        endpoint returns status code 404 if the department is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/department/1',
                          data=json.dumps({
                              'department_name': 'new_test_d',
                              'organization_id': self.d_dict['organization_id']
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_dept_delete_with_authentication(self):
        """
        Test that a DELETE request to the /department/<int:department_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/department/{self.get_department_id()}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_dept_delete_without_authentication(self):
        """
        Test that a DELETE request to the /department/<int:department_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/department/{self.get_department_id()}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_dept_delete_inactive(self):
        """
        Test that a DELETE request to the /department/<int:department_id>
        endpoint returns status code 400 if the department is already inactive.
        """
        with self.app() as c:
            with self.app_context():
                department_id = self.get_department_id()

                # Make department inactive.
                c.delete(f'/department/{department_id}',
                         headers=self.get_headers())

                # Send DELETE request on inactive department.
                r = c.delete(f'/department/{department_id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_dept_delete_not_found(self):
        """
        Test that a DELETE request to the /department/<int:department_id>
        endpoint returns status code 404 if the department is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/department/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_activate_dept_with_authentication(self):
        """
        Test that a PUT request to the /activate_department/<int:department_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                department_id = self.get_department_id()

                c.delete(f'/department/{department_id}',
                         headers=self.get_headers())

                r = c.put(f'/activate_department/{department_id}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_activate_dept_without_authentication(self):
        """
        Test that a PUT request to the /activate_department/<int:department_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_department with
                # wrong authorization header.
                r = c.put(f'/activate_department/{self.get_department_id()}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_activate_dept_active(self):
        """
        Test that a PUT request to the /activate_department/<int:department_id>
        endpoint returns status code 400 if the department is already active.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_department/{self.get_department_id()}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_activate_dept_not_found(self):
        """
        Test that a PUT request to the /activate_department/<int:department_id>
        endpoint returns status code 404 if the department is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_department/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
