import json

from models.employment_position import EmploymentPositionModel
from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestEmploymentPosition(BaseTest):
    """System tests for the employment_position resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a dict representing
        an employement_position and instantiating an OrganizationModel
        object and saving it to the db so they are available for the
        different tests.
        """
        super(TestEmploymentPosition, self).setUp()
        with self.app_context():
            OrganizationModel('test_o', True).save_to_db()

            self.e_p_dict = {
                'position_name_feminine': 'test_e_p_f',
                'position_name_masculine': 'test_e_p_m',
                'minimum_hourly_wage': 1.00,
                'organization_id': OrganizationModel.find_by_name('test_o').id,
                'is_active': True
            }

    def test_emp_pos_post_with_authentication(self):
        """
        Test that a POST request to the /employment_position endpoint
        returns status code 201 and that the department is present in the
        database after the POST request.
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

                self.assertEqual(r.status_code, 201)

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
        Test that a GET request to the
        /employment_position/<string:position_name/organization_id>
        endpoint returns the correct employment_position if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/employment_position',
                       data=json.dumps(self.e_p_dict),
                       headers=self.get_headers())

                # Send GET request to the endpoint.
                r = c.get(f'employment_position/test_e_p_f'
                          f'/{self.e_p_dict["organization_id"]}',
                          headers=self.get_headers())

                r_dict = json.loads(r.data)

                self.assertEqual(r.status_code, 200)

                self.assertEqual(r_dict['position_name_feminine'],
                                 self.e_p_dict['position_name_feminine'])

    def test_emp_pos_get_not_found(self):
        """
        Test that a GET request to the
        /employment_position/<string:position_name/organization_id>
        endpoint returns status code 404 if the employment_position
        is not found in the database table.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint.
                r = c.get(f'/employment_position/test_e_p_f'
                          f'/{self.e_p_dict["organization_id"]}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_emp_pos_get_without_authentication(self):
        """
        Test that a GET request to the
        /employment_position/<string:position_name/organization_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/employment_position/test_e_p_f'
                          f'/{self.e_p_dict["organization_id"]}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)
