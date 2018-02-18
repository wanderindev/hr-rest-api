import json

from models.shift import ShiftModel
from tests.base_test import BaseTest


class TestShift(BaseTest):
    """System tests for the shift resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating two dicts representing
        a rotating shift and a fixed shift so they are available for the
        different tests.
        """
        super(TestShift, self).setUp()
        with self.app_context():
            self.s_r_dict = {
                'shift_name': 'test_s_r',
                'weekly_hours': 48,
                'is_rotating': True,
                'payment_period': 'Quincenal',
                'break_length': '00:30:00',
                'is_break_included_in_shift': False,
                'is_active': True,
                'organization_id': 1,
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
                'organization_id': 1,
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
                self.assertIsNone(ShiftModel
                                  .find_by_name(self.s_r_dict['shift_name'],
                                                self.s_r_dict[
                                                    'organization_id']))
                self.assertIsNone(ShiftModel
                                  .find_by_name(self.s_f_dict['shift_name'],
                                                self.s_f_dict[
                                                    'organization_id']))

                # Send POST request with rotating shift.
                r = c.post('/shift',
                           data=json.dumps(self.s_r_dict),
                           headers=self.get_headers())

                r_shift = json.loads(r.data)['shift']

                self.assertTrue(r_shift['is_active'])
                self.assertTrue(r_shift['is_rotating'])
                self.assertEqual(r_shift['payment_period'],
                                 self.s_r_dict['payment_period'])
                self.assertEqual(r_shift['rotation_start_hour'],
                                 self.s_r_dict['rotation_start_hour'])
                self.assertEqual(r_shift['rotation_end_hour'],
                                 self.s_r_dict['rotation_end_hour'])
                self.assertEqual(r_shift['break_length'],
                                 self.s_r_dict['break_length'])
                self.assertEqual(r_shift['shift_name'],
                                 self.s_r_dict['shift_name'])
                self.assertEqual(float(r_shift['weekly_hours']),
                                 self.s_r_dict['weekly_hours'])
                self.assertEqual(r_shift['organization_id'],
                                 self.s_r_dict['organization_id'])
                self.assertListEqual(r_shift['employees'], [])
                self.assertEqual(r.status_code, 201)
                self.assertIsNotNone(ShiftModel
                                     .find_by_name(self.s_r_dict['shift_name'],
                                                   self.s_r_dict[
                                                       'organization_id']))

                # Send POST request with fixed shift.
                r = c.post('/shift',
                           data=json.dumps(self.s_f_dict),
                           headers=self.get_headers())

                r_shift = json.loads(r.data)['shift']

                self.assertEqual(r_shift['rest_day'],
                                 self.s_f_dict['rest_day'])
                self.assertEqual(r_shift['fixed_start_hour_monday'],
                                 self.s_f_dict['fixed_start_hour_monday'])
                self.assertEqual(r_shift['fixed_start_hour_tuesday'],
                                 self.s_f_dict['fixed_start_hour_tuesday'])
                self.assertEqual(r_shift['fixed_start_hour_wednesday'],
                                 self.s_f_dict['fixed_start_hour_wednesday'])
                self.assertEqual(r_shift['fixed_start_hour_thursday'],
                                 self.s_f_dict['fixed_start_hour_thursday'])
                self.assertEqual(r_shift['fixed_start_hour_friday'],
                                 self.s_f_dict['fixed_start_hour_friday'])
                self.assertEqual(r_shift['fixed_start_hour_saturday'],
                                 self.s_f_dict['fixed_start_hour_saturday'])
                self.assertIsNone(r_shift['fixed_start_hour_sunday'])
                self.assertEqual(r_shift['fixed_start_break_hour_monday'],
                                 self.s_f_dict['fixed_start_break_hour_monday'])
                self.assertEqual(r_shift['fixed_start_break_hour_tuesday'],
                                 self.s_f_dict[
                                     'fixed_start_break_hour_tuesday'])
                self.assertEqual(r_shift['fixed_start_break_hour_wednesday'],
                                 self.s_f_dict[
                                     'fixed_start_break_hour_wednesday'])
                self.assertEqual(r_shift['fixed_start_break_hour_thursday'],
                                 self.s_f_dict[
                                     'fixed_start_break_hour_thursday'])
                self.assertEqual(r_shift['fixed_start_break_hour_friday'],
                                 self.s_f_dict['fixed_start_break_hour_friday'])
                self.assertIsNone(r_shift['fixed_start_break_hour_saturday'])
                self.assertIsNone(r_shift['fixed_start_break_hour_sunday'])
                self.assertEqual(r_shift['fixed_end_break_hour_monday'],
                                 self.s_f_dict['fixed_end_break_hour_monday'])
                self.assertEqual(r_shift['fixed_end_break_hour_tuesday'],
                                 self.s_f_dict['fixed_end_break_hour_tuesday'])
                self.assertEqual(r_shift['fixed_end_break_hour_wednesday'],
                                 self.s_f_dict[
                                     'fixed_end_break_hour_wednesday'])
                self.assertEqual(r_shift['fixed_end_break_hour_thursday'],
                                 self.s_f_dict['fixed_end_break_hour_thursday'])
                self.assertEqual(r_shift['fixed_end_break_hour_friday'],
                                 self.s_f_dict['fixed_end_break_hour_friday'])
                self.assertIsNone(r_shift['fixed_end_break_hour_saturday'])
                self.assertIsNone(r_shift['fixed_end_break_hour_sunday'])
                self.assertEqual(r_shift['fixed_end_hour_monday'],
                                 self.s_f_dict['fixed_end_hour_monday'])
                self.assertEqual(r_shift['fixed_end_hour_tuesday'],
                                 self.s_f_dict['fixed_end_hour_tuesday'])
                self.assertEqual(r_shift['fixed_end_hour_wednesday'],
                                 self.s_f_dict['fixed_end_hour_wednesday'])
                self.assertEqual(r_shift['fixed_end_hour_thursday'],
                                 self.s_f_dict['fixed_end_hour_thursday'])
                self.assertEqual(r_shift['fixed_end_hour_friday'],
                                 self.s_f_dict['fixed_end_hour_friday'])
                self.assertEqual(r_shift['fixed_end_hour_saturday'],
                                 self.s_f_dict['fixed_end_hour_saturday'])
                self.assertIsNone(r_shift['fixed_end_hour_sunday'])
                self.assertEqual(r.status_code, 201)
                self.assertIsNotNone(ShiftModel
                                     .find_by_name(self.s_f_dict['shift_name'],
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
        POST duplicated data to the /shift endpoint.
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
        Test that a GET request to the /shift/<string:shift_name> endpoint
        returns the correct shift if the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/shift',
                       data=json.dumps(self.s_r_dict),
                       headers=self.get_headers())

                r = c.get(f'/shift/{self.s_r_dict["shift_name"]}',
                          headers=self.get_headers())

                r_dict = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(r_dict['shift_name'],
                                 self.s_r_dict['shift_name'])

    def test_shift_get_not_found(self):
        """
        Test that a GET request to the /shift/<string:shift_name>
        endpoint returns status code 404 if the shift is not found
        in the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/shift/{self.s_r_dict["shift_name"]}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_shift_get_without_authentication(self):
        """
        Test that a GET request to the /shift/<string:shift_name>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/shift/{self.s_r_dict["shift_name"]}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_shift_put_with_authentication(self):
        """
        Test that a PUT request to the /shift/<string:shift_name>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post(f'/shift',
                       data=json.dumps(self.s_r_dict),
                       headers=self.get_headers())

                c.post(f'/shift',
                       data=json.dumps(self.s_f_dict),
                       headers=self.get_headers())

                # Send PUT request modifying the rotating shift.
                r = c.put(f'/shift/{self.s_r_dict["shift_name"]}',
                          data=json.dumps({
                              'shift_name': 'new_test_s_r',
                              'weekly_hours': 44,
                              'is_rotating': True,
                              'payment_period': 'Semanal',
                              'break_length': '01:00:00',
                              'is_break_included_in_shift': True,
                              'is_active': True,
                              'organization_id': self.s_r_dict[
                                  'organization_id'],
                              'rotation_start_hour': '00:00:00',
                              'rotation_end_hour': '15:00:00'
                          }),
                          headers=self.get_headers())

                r_shift = json.loads(r.data)['shift']

                self.assertTrue(r_shift['is_active'])
                self.assertTrue(r_shift['is_rotating'])
                self.assertEqual(r_shift['payment_period'],
                                 'Semanal')
                self.assertEqual(r_shift['rotation_start_hour'],
                                 '00:00:00')
                self.assertEqual(r_shift['rotation_end_hour'],
                                 '15:00:00')
                self.assertEqual(r_shift['break_length'],
                                 '01:00:00')
                self.assertEqual(r_shift['shift_name'],
                                 'new_test_s_r')
                self.assertEqual(float(r_shift['weekly_hours']),
                                 44)
                self.assertEqual(r_shift['organization_id'],
                                 self.s_r_dict['organization_id'])
                self.assertListEqual(r_shift['employees'], [])
                self.assertEqual(r.status_code, 200)

                # Send PUT request modifying the fixed shift.
                r = c.put(f'/shift/{self.s_f_dict["shift_name"]}',
                          data=json.dumps({
                              'shift_name': 'test_s_f',
                              'weekly_hours': 48,
                              'is_rotating': False,
                              'payment_period': 'Diario',
                              'break_length': '00:30:00',
                              'is_break_included_in_shift': False,
                              'is_active': True,
                              'organization_id': self.s_f_dict[
                                  'organization_id'],
                              'fixed_start_hour_sunday': '09:00:00',
                              'fixed_start_break_hour_sunday': '13:00:00',
                              'fixed_end_break_hour_sunday': '13:30:00',
                              'fixed_end_hour_sunday': '17:30:00',
                              'fixed_start_hour_monday': '09:00:00',
                              'fixed_start_break_hour_monday': '13:00:00',
                              'fixed_end_break_hour_monday': '13:30:00',
                              'fixed_end_hour_monday': '17:30:00',
                              'fixed_start_hour_tuesday': '09:00:00',
                              'fixed_start_break_hour_tuesday': '13:00:00',
                              'fixed_end_break_hour_tuesday': '13:30:00',
                              'fixed_end_hour_tuesday': '17:30:00',
                              'fixed_start_hour_wednesday': '09:00:00',
                              'fixed_start_break_hour_wednesday': '13:00:00',
                              'fixed_end_break_hour_wednesday': '13:30:00',
                              'fixed_end_hour_wednesday': '17:30:00',
                              'fixed_start_hour_thursday': '09:00:00',
                              'fixed_start_break_hour_thursday': '13:00:00',
                              'fixed_end_break_hour_thursday': '13:30:00',
                              'fixed_end_hour_thursday': '17:30:00',
                              'fixed_start_hour_friday': '09:00:00',
                              'fixed_start_break_hour_friday': '13:00:00',
                              'fixed_end_break_hour_friday': '13:30:00',
                              'fixed_end_hour_friday': '17:30:00',
                              'fixed_start_hour_saturday': None,
                              'fixed_end_hour_saturday': None,
                              'rest_day': 'Sábado'
                          }),
                          headers=self.get_headers())

                r_shift = json.loads(r.data)['shift']

                self.assertEqual(r_shift['rest_day'],
                                 'Sábado')
                self.assertEqual(r_shift['fixed_start_hour_monday'],
                                 '09:00:00')
                self.assertEqual(r_shift['fixed_start_hour_tuesday'],
                                 '09:00:00')
                self.assertEqual(r_shift['fixed_start_hour_wednesday'],
                                 '09:00:00')
                self.assertEqual(r_shift['fixed_start_hour_thursday'],
                                 '09:00:00')
                self.assertEqual(r_shift['fixed_start_hour_friday'],
                                 '09:00:00')
                self.assertIsNone(r_shift['fixed_start_hour_saturday'])
                self.assertEqual(r_shift['fixed_start_hour_sunday'],
                                 '09:00:00')
                self.assertEqual(r_shift['fixed_start_break_hour_monday'],
                                 '13:00:00')
                self.assertEqual(r_shift['fixed_start_break_hour_tuesday'],
                                 '13:00:00')
                self.assertEqual(r_shift['fixed_start_break_hour_wednesday'],
                                 '13:00:00')
                self.assertEqual(r_shift['fixed_start_break_hour_thursday'],
                                 '13:00:00')
                self.assertEqual(r_shift['fixed_start_break_hour_friday'],
                                 '13:00:00')
                self.assertIsNone(r_shift['fixed_start_break_hour_saturday'])

                self.assertEqual(r_shift['fixed_start_break_hour_sunday'],
                                 '13:00:00')
                self.assertEqual(r_shift['fixed_end_break_hour_monday'],
                                 '13:30:00')
                self.assertEqual(r_shift['fixed_end_break_hour_tuesday'],
                                 '13:30:00')
                self.assertEqual(r_shift['fixed_end_break_hour_wednesday'],
                                 '13:30:00')
                self.assertEqual(r_shift['fixed_end_break_hour_thursday'],
                                 '13:30:00')
                self.assertEqual(r_shift['fixed_end_break_hour_friday'],
                                 '13:30:00')
                self.assertIsNone(r_shift['fixed_end_break_hour_saturday'])
                self.assertEqual(r_shift['fixed_end_break_hour_sunday'],
                                 '13:30:00')
                self.assertEqual(r_shift['fixed_end_hour_monday'],
                                 '17:30:00')
                self.assertEqual(r_shift['fixed_end_hour_tuesday'],
                                 '17:30:00')
                self.assertEqual(r_shift['fixed_end_hour_wednesday'],
                                 '17:30:00')
                self.assertEqual(r_shift['fixed_end_hour_thursday'],
                                 '17:30:00')
                self.assertEqual(r_shift['fixed_end_hour_friday'],
                                 '17:30:00')
                self.assertIsNone(r_shift['fixed_end_hour_saturday'])
                self.assertEqual(r_shift['fixed_end_hour_sunday'],
                                 '17:30:00')
                self.assertEqual(r.status_code, 200)

    def test_shift_put_without_authentication(self):
        """
        Test that a PUT request to the /shift/<string:shift_name>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/shift/{self.s_r_dict["shift_name"]}',
                          data=json.dumps({
                              'shift_name': 'new_test_s_r',
                              'weekly_hours': 44,
                              'is_rotating': True,
                              'payment_period': 'Semanal',
                              'break_length': '01:00:00',
                              'is_break_included_in_shift': True,
                              'is_active': True,
                              'organization_id': self.s_r_dict[
                                  'organization_id'],
                              'rotation_start_hour': '00:00:00',
                              'rotation_end_hour': '15:00:00'
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_shift_put_not_found(self):
        """
        Test that a PUT request to the /shift/<string:shift_name> endpoint
        returns status code 404 if the shift is not in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/shift/{self.s_r_dict["shift_name"]}',
                          data=json.dumps({
                              'shift_name': 'new_test_s_r',
                              'weekly_hours': 44,
                              'is_rotating': True,
                              'payment_period': 'Semanal',
                              'break_length': '01:00:00',
                              'is_break_included_in_shift': True,
                              'is_active': True,
                              'organization_id': self.s_r_dict[
                                  'organization_id'],
                              'rotation_start_hour': '00:00:00',
                              'rotation_end_hour': '15:00:00'
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_shift_delete_with_authentication(self):
        """
        Test that a DELETE request to the /shift/<string:shift_name>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/shift',
                       data=json.dumps(self.s_r_dict),
                       headers=self.get_headers())

                r = c.delete(f'/shift/{self.s_r_dict["shift_name"]}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_shift_delete_without_authentication(self):
        """
        Test that a DELETE request to the /shift/<string:shift_name>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/shift/{self.s_r_dict["shift_name"]}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_shift_delete_inactive(self):
        """
        Test that a DELETE request to the /shift/<string:shift_name>
        endpoint returns status code 400 if the shift is already inactive.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/shift',
                       data=json.dumps(self.s_r_dict),
                       headers=self.get_headers())

                # Make shift inactive.
                c.delete(f'/shift/{self.s_r_dict["shift_name"]}',
                         headers=self.get_headers())

                # Send DELETE request on inactive shift.
                r = c.delete(f'/shift/{self.s_r_dict["shift_name"]}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_shift_delete_not_found(self):
        """
        Test that a DELETE request to the /shift/<string:shift_name>
        endpoint returns status code 404 if the shift is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/shift/{self.s_r_dict["shift_name"]}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_activate_shift_with_authentication(self):
        """
        Test that a PUT request to the /activate_shift/<string:shift_name>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/shift',
                       data=json.dumps(self.s_r_dict),
                       headers=self.get_headers())

                c.delete(f'/shift/{self.s_r_dict["shift_name"]}',
                         headers=self.get_headers())

                r = c.put(f'/activate_shift/{self.s_r_dict["shift_name"]}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_activate_shift_without_authentication(self):
        """
        Test that a PUT request to the /activate_shift/<string:shift_name>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_shift with
                # wrong authorization header.
                r = c.put(f'/activate_shift/{self.s_r_dict["shift_name"]}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_activate_shift_active(self):
        """
        Test that a PUT request to the /activate_shift/<string:shift_name>
        endpoint returns status code 400 if the shift is already active.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/shift',
                       data=json.dumps(self.s_r_dict),
                       headers=self.get_headers())

                r = c.put(f'/activate_shift/{self.s_r_dict["shift_name"]}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_activate_shift_not_found(self):
        """
        Test that a PUT request to the /activate_shift/<string:shift_name>
        endpoint returns status code 404 if the shift is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_shift/{self.s_r_dict["shift_name"]}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
