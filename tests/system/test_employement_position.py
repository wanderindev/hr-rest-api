import json

from models.employment_position import EmploymentPositionModel
from tests.base_test import BaseTest


class TestEmploymentPosition(BaseTest):
    """System tests for the employment_position resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a dict representing
        an employment_position so it is available for the different tests.
        """
        super(TestEmploymentPosition, self).setUp()
        with self.app_context():
            self.e_p_dict = {
                'position_name_feminine': 'test_e_p_f',
                'position_name_masculine': 'test_e_p_m',
                'minimum_hourly_wage': 1.00,
                'is_active': True,
                'organization_id': 1
            }

    def test_emp_pos_post_with_authentication(self):
        """
        Test that a POST request to the /employment_position endpoint
        returns status code 201 and that the employment_position
        is present in the database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                # Check that 'test_e_p_f' is not in the database.
                self.assertIsNone(EmploymentPositionModel
                                  .find_by_name('test_e_p_f',
                                                self.e_p_dict[
                                                    'organization_id']))

                # Send POST request to the /employment_position endpoint.
                r = c.post('/employment_position',
                           data=json.dumps(self.e_p_dict),
                           headers=self.get_headers())

                r_e_p = json.loads(r.data)['employment_position']

                self.assertEqual(r.status_code, 201)

                self.assertTrue(r_e_p['is_active'])

                self.assertEqual(r_e_p['position_name_feminine'],
                                 self.e_p_dict['position_name_feminine'])

                self.assertEqual(r_e_p['position_name_masculine'],
                                 self.e_p_dict['position_name_masculine'])

                self.assertEqual(float(r_e_p['minimum_hourly_wage']),
                                 self.e_p_dict['minimum_hourly_wage'])

                self.assertEqual(r_e_p['organization_id'],
                                 self.e_p_dict['organization_id'])

                self.assertListEqual(r_e_p['employees'], [])

                self.assertIsNotNone(EmploymentPositionModel
                                     .find_by_name('test_e_p_f',
                                                   self.e_p_dict[
                                                       'organization_id']))

    def test_emp_pos_post_without_authentication(self):
        """
        Test that a POST request to the /employment_position endpoint
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /employment_position endpoint with
                # wrong authentication header.
                r = c.post('/employment_position',
                           data=json.dumps(self.e_p_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_emp_pos_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicate data to the /employment_position endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/employment_position',
                       data=json.dumps(self.e_p_dict),
                       headers=self.get_headers())

                # Send duplicated POST request.
                r = c.post('/employment_position',
                           data=json.dumps(self.e_p_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_emp_pos_get_with_authentication(self):
        """
        Test that a GET request to the /employment_position
        /<string:position_name> endpoint returns the correct
        employment_position if the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/employment_position',
                       data=json.dumps(self.e_p_dict),
                       headers=self.get_headers())

                # Send GET request to the endpoint.
                r = c.get(f'employment_position/test_e_p_f',
                          headers=self.get_headers())

                r_dict = json.loads(r.data)

                self.assertEqual(r.status_code, 200)

                self.assertEqual(r_dict['position_name_feminine'],
                                 self.e_p_dict['position_name_feminine'])

    def test_emp_pos_get_not_found(self):
        """
        Test that a GET request to the /employment_position
        /<string:position_name> endpoint returns status code
        404 if the employment_position is not found in the
        database table.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint.
                r = c.get(f'/employment_position/test_e_p_f',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_emp_pos_get_without_authentication(self):
        """
        Test that a GET request to the /employment_position
        /<string:position_name> returns status code 401 if
        the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/employment_position/test_e_p_f',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_emp_pos_put_with_authentication(self):
        """
        Test that a PUT request to the /employment_position
        /<string:position_name> endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post(f'/employment_position',
                       data=json.dumps(self.e_p_dict),
                       headers=self.get_headers())

                # Send PUT request to the endpoint.
                r = c.put(f'/employment_position/test_e_p_f',
                          data=json.dumps({
                              'position_name_feminine': 'new_test_e_p_f',
                              'position_name_masculine': 'new_test_e_p_m',
                              'minimum_hourly_wage': 2.00,
                              'organization_id': self.e_p_dict[
                                  'organization_id'],
                              'is_active': True
                          }),
                          headers=self.get_headers())

                r_e_p = json.loads(r.data)['employment_position']

                self.assertEqual(r.status_code, 200)

                self.assertTrue(r_e_p['is_active'])

                self.assertEqual(r_e_p['position_name_feminine'],
                                 'new_test_e_p_f')

                self.assertEqual(r_e_p['position_name_masculine'],
                                 'new_test_e_p_m')

                self.assertEqual(float(r_e_p['minimum_hourly_wage']),
                                 2.00)

                self.assertEqual(r_e_p['organization_id'],
                                 self.e_p_dict['organization_id'])

                self.assertListEqual(r_e_p['employees'], [])

                self.assertEqual(r.status_code, 200)

    def test_emp_pos_put_without_authentication(self):
        """
        Test that a PUT request to the /employment_position
        /<string:position_name> endpoint returns status code
        401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/employment_position/test_e_p_f',
                          data=json.dumps({
                              'position_name_feminine': 'new_test_e_p_f',
                              'position_name_masculine': 'new_test_e_p_m',
                              'minimum_hourly_wage': 2.00,
                              'organization_id': self.e_p_dict[
                                  'organization_id'],
                              'is_active': True
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_emp_pos_put_not_found(self):
        """
        Test that a PUT request to the /employment_position
        /<string:position_name> endpoint returns status code
        404 if the employment_position is not in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/employment_position/test_e_p_f',
                          data=json.dumps({
                              'position_name_feminine': 'new_test_e_p_f',
                              'position_name_masculine': 'new_test_e_p_m',
                              'minimum_hourly_wage': 2.00,
                              'organization_id': self.e_p_dict[
                                  'organization_id'],
                              'is_active': True
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_emp_pos_delete_with_authentication(self):
        """
        Test that a DELETE request to the /employment_position
        /<string:position_name> endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/employment_position',
                       data=json.dumps(self.e_p_dict),
                       headers=self.get_headers())

                # Send DELETE request to the endpoint.
                r = c.delete(f'/employment_position/test_e_p_f',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_emp_pos_delete_without_authentication(self):
        """
        Test that a DELETE request to the /employment_position
        /<string:position_name> endpoint returns status code
        401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/employment_position/test_e_p_f',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_emp_pos_delete_inactive(self):
        """
        Test that a DELETE request to the /employment_position
        /<string:position_name> endpoint returns status code 400
        if the employment_position is already inactive.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/employment_position',
                       data=json.dumps(self.e_p_dict),
                       headers=self.get_headers())

                # Make employment_position inactive.
                c.delete(f'/employment_position/test_e_p_f',
                         headers=self.get_headers())

                # Try DELETE on inactive employment_position.
                r = c.delete(f'/employment_position/test_e_p_f',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_emp_pos_delete_not_found(self):
        """
        Test that a DELETE request to the /employment_position
        /<string:position_name> endpoint returns status code
        404 if the employment_position is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/employment_position/test_e_p_f',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_activate_emp_pos_with_authentication(self):
        """
        Test that a PUT request to the /activate_employment_position
        /<string:position_name> endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/employment_position',
                       data=json.dumps(self.e_p_dict),
                       headers=self.get_headers())

                # Make employment_position inactive.
                c.delete(f'/employment_position/test_e_p_f',
                         headers=self.get_headers())

                # Send PUT request to /activate_employment_position
                r = c.put(f'/activate_employment_position/test_e_p_f',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_activate_emp_pos_without_authentication(self):
        """
        Test that a PUT request to the /activate_employment_position
        /<string:position_name> endpoint returns status code 401
        if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to activate_employment_position
                # with wrong authorization header.
                r = c.put(f'/activate_employment_position/test_e_p_f',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_activate_emp_pos_active(self):
        """
        Test that a PUT request to the /activate_employment_position
        /<string:position_name> endpoint returns status code 400 if
        the employment_position is already active.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/employment_position',
                       data=json.dumps(self.e_p_dict),
                       headers=self.get_headers())

                # Send PUT request to /activate_employment_position
                r = c.put(f'/activate_employment_position/test_e_p_f',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_activate_emp_pos_not_found(self):
        """
        Test that a PUT request to the /activate_employment_position
        /<string:position_name> endpoint returns status code 404
        if the employment_position is not found.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_employment_position
                r = c.put(f'/activate_employment_position/test_e_p_f',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
