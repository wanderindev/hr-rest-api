import json

from models.organization import OrganizationModel
from models.shift import ShiftModel
from tests.base_test import BaseTest


class TestShift(BaseTest):
    """System tests for the shift resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating two dicts representing
        a rotating shift and a fixed shift and instantiating an
        OrganizationModel object and saving it to the db so they are
        available for the different tests.
        """
        super(TestShift, self).setUp()
        with self.app_context():
            OrganizationModel('test_o', True).save_to_db()

            self.s_r_dict = {
                'shift_name': 'test_s_r',
                'weekly_hours': 48,
                'is_rotating': True,
                'payment_period': 'Quincenal',
                'break_length': '00:30:00',
                'is_break_included_in_shift': False,
                'is_active': True,
                'organization_id': OrganizationModel.find_by_name('test_o').id,
                'rotation_start_hour': '06:00:00',
                'rotation_end_hour': '21:00:00'
            }

            self.s_f_dict = {
                'shift_name': 'test_s_f',
                'weekly_hours': 44,
                'is_rotating': False,
                'payment_period': 'Quincenal',
                'break_length': '00:30:00',
                'is_break_included_in_shift': False,
                'is_active': True,
                'organization_id': OrganizationModel.find_by_name('test_o').id,
                'fixed_start_hour_monday': '08:00:00',
                'fixed_start_break_hour_monday': '12:00:00',
                'fixed_end_break_hour_monday': '12:30:00',
                'fixed_end_hour_monday': '16:30:00',
                'fixed_start_hour_tuesday': '08:00:00',
                'fixed_start_break_hour_tuesday': '12:00:00',
                'fixed_end_break_hour_tuesday': '12:30:00',
                'fixed_end_hour_tuesday': '16:30:00',
                'fixed_start_hour_wednesday': '08:00:00',
                'fixed_start_break_hour_wednesday': '12:00:00',
                'fixed_end_break_hour_wednesday': '12:30:00',
                'fixed_end_hour_wednesday': '16:30:00',
                'fixed_start_hour_thursday': '08:00:00',
                'fixed_start_break_hour_thursday': '12:00:00',
                'fixed_end_break_hour_thursday': '12:30:00',
                'fixed_end_hour_thursday': '16:30:00',
                'fixed_start_hour_friday': '08:00:00',
                'fixed_start_break_hour_friday': '12:00:00',
                'fixed_end_break_hour_friday': '12:30:00',
                'fixed_end_hour_friday': '16:30:00',
                'fixed_start_hour_saturday': '08:00:00',
                'fixed_end_hour_saturday': '12:00:00',
                'rest_day': 'Domingo'
            }

    def test_shift_post_with_authentication(self):
        """
        Test that a POST request to the /shift endpoint returns
        status code 201 and that the shift is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                # Check that 'test_s_r'  and 'test_s_f'
                # are not in the database.
                self.assertIsNone(ShiftModel
                                  .find_by_name('test_s_r',
                                                self.s_r_dict[
                                                    'organization_id']))
                self.assertIsNone(ShiftModel
                                  .find_by_name('test_s_f',
                                                self.s_f_dict[
                                                    'organization_id']))

                # Send POST request to the /shift endpoint.
                r = c.post('/shift',
                           data=json.dumps(self.s_r_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 201)

                self.assertIsNotNone(ShiftModel
                                     .find_by_name('test_s_r',
                                                   self.s_r_dict[
                                                       'organization_id']))

                # Send POST request to the /shift endpoint.
                r = c.post('/shift',
                           data=json.dumps(self.s_f_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 201)

                self.assertIsNotNone(ShiftModel
                                     .find_by_name('test_s_f',
                                                   self.s_f_dict[
                                                       'organization_id']))

    def test_shift_post_without_authentication(self):
        """
        Test that a POST request to the /shift endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /shift endpoint with
                # wrong authentication header.
                r = c.post('/shift',
                           data=json.dumps(self.s_r_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_shift_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicate data to the /shift endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/shift',
                       data=json.dumps(self.s_r_dict),
                       headers=self.get_headers())

                # Send duplicated POST request.
                r = c.post('/shift',
                           data=json.dumps(self.s_r_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_shift_get_with_authentication(self):
        """
        Test that a GET request to the
        /shift/<string:shift_name/organization_id>
        endpoint returns the correct shift if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/shift',
                       data=json.dumps(self.s_r_dict),
                       headers=self.get_headers())

                # Send GET request to the endpoint.
                r = c.get(f'/shift/test_s_r'
                          f'/{self.s_r_dict["organization_id"]}',
                          headers=self.get_headers())

                r_dict = json.loads(r.data)

                self.assertEqual(r.status_code, 200)

                self.assertEqual(r_dict['shift_name'],
                                 self.s_r_dict['shift_name'])

    def test_shift_get_not_found(self):
        """
        Test that a GET request to the
        /shift/<string:shift_name/organization_id>
        endpoint returns status code 404 if the shift
        is not found in the database table.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint.
                r = c.get(f'/shift/test_s_r'
                          f'/{self.s_r_dict["organization_id"]}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_shift_get_without_authentication(self):
        """
        Test that a GET request to the
        /shift/<string:shift_name/organization_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/shift/test_s_r'
                          f'/{self.s_r_dict["organization_id"]}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)
