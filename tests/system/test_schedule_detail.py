import json

from models.schedule_detail import ScheduleDetailModel
from tests.base_test import BaseTest


class TestScheduleDetail(BaseTest):
    """System tests for the schedule detail resource."""

    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a
        dict representing an schedule detail.
        """
        super(TestScheduleDetail, self).setUp()

        with self.app_context():
            self.sch_d_dict = {
                'day_1_start': '2018-01-01T06:00:00',
                'day_1_end': '2018-01-01T14:00:00',
                'day_1_comment': 'comment 1',
                'day_2_start': '2018-01-02T06:00:00',
                'day_2_end': '2018-01-02T14:00:00',
                'day_2_comment': 'comment 2',
                'day_3_start': '2018-01-03T06:00:00',
                'day_3_end': '2018-01-03T14:00:00',
                'day_3_comment': 'comment 3',
                'day_4_start': '2018-01-04T06:00:00',
                'day_4_end': '2018-01-04T14:00:00',
                'day_4_comment': 'comment 4',
                'day_5_start': None,
                'day_5_end': None,
                'day_5_comment': None,
                'day_6_start': '2018-01-06T22:00:00',
                'day_6_end': '2018-01-07T06:00:00',
                'day_6_comment': 'comment 6',
                'day_7_start': '2018-01-07T22:00:00',
                'day_7_end': '2018-01-08T06:00:00',
                'day_7_comment': 'comment 7',
                'employee_id': self.get_employee().id,
                'schedule_id': self.get_schedule().id
            }

    def test_sch_d_post_with_authentication(self):
        """
        Test that a POST request to the /schedule_detail endpoint returns
        status code 201 and that the schedule detail is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/schedule_detail',
                           data=json.dumps(self.sch_d_dict),
                           headers=self.get_headers())

                sch_d = json.loads(r.data)['schedule_detail']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(sch_d['day_1_start'],
                                 self.sch_d_dict['day_1_start'])
                self.assertEqual(sch_d['day_1_end'],
                                 self.sch_d_dict['day_1_end'])
                self.assertEqual(sch_d['day_1_comment'],
                                 self.sch_d_dict['day_1_comment'])
                self.assertEqual(sch_d['day_2_start'],
                                 self.sch_d_dict['day_2_start'])
                self.assertEqual(sch_d['day_2_end'],
                                 self.sch_d_dict['day_2_end'])
                self.assertEqual(sch_d['day_2_comment'],
                                 self.sch_d_dict['day_2_comment'])
                self.assertEqual(sch_d['day_3_start'],
                                 self.sch_d_dict['day_3_start'])
                self.assertEqual(sch_d['day_3_end'],
                                 self.sch_d_dict['day_3_end'])
                self.assertEqual(sch_d['day_3_comment'],
                                 self.sch_d_dict['day_3_comment'])
                self.assertEqual(sch_d['day_4_start'],
                                 self.sch_d_dict['day_4_start'])
                self.assertEqual(sch_d['day_4_end'],
                                 self.sch_d_dict['day_4_end'])
                self.assertEqual(sch_d['day_4_comment'],
                                 self.sch_d_dict['day_4_comment'])
                self.assertEqual(sch_d['day_5_start'],
                                 self.sch_d_dict['day_5_start'])
                self.assertEqual(sch_d['day_5_end'],
                                 self.sch_d_dict['day_5_end'])
                self.assertEqual(sch_d['day_5_comment'],
                                 self.sch_d_dict['day_5_comment'])
                self.assertEqual(sch_d['day_6_start'],
                                 self.sch_d_dict['day_6_start'])
                self.assertEqual(sch_d['day_6_end'],
                                 self.sch_d_dict['day_6_end'])
                self.assertEqual(sch_d['day_6_comment'],
                                 self.sch_d_dict['day_6_comment'])
                self.assertEqual(sch_d['day_7_start'],
                                 self.sch_d_dict['day_7_start'])
                self.assertEqual(sch_d['day_7_end'],
                                 self.sch_d_dict['day_7_end'])
                self.assertEqual(sch_d['day_7_comment'],
                                 self.sch_d_dict['day_7_comment'])
                self.assertEqual(sch_d['employee_id'],
                                 self.sch_d_dict['employee_id'])
                self.assertEqual(sch_d['schedule_id'],
                                 self.sch_d_dict['schedule_id'])
                self.assertIsNotNone(ScheduleDetailModel.find_by_id(sch_d['id'],
                                                                    self.u))

    def test_sch_d_post_without_authentication(self):
        """
        Test that a POST request to the /schedule_detail endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /schedule_detail endpoint with
                # wrong authentication header.
                r = c.post('/schedule_detail',
                           data=json.dumps(self.sch_d_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_sch_d_post_wrong_user(self):
        """
        Test that status code 403 is returned when trying to POST an
        schedule detail with a user without permission.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/schedule_detail',
                           data=json.dumps(self.sch_d_dict),
                           headers=self.get_headers({
                               'username': 'test_other_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 403)

    def test_sch_d_get_with_authentication(self):
        """
        Test that a GET request to the /schedule_detail/<int:detail_id>
        endpoint returns the correct schedule detail and status code 200 if
        the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/schedule_detail/{self.get_schedule_detail().id}',
                          headers=self.get_headers())

                sch_d = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(sch_d['day_1_start'],
                                 self.sch_d_dict['day_1_start'])
                self.assertEqual(sch_d['day_1_end'],
                                 self.sch_d_dict['day_1_end'])
                self.assertEqual(sch_d['day_1_comment'],
                                 self.sch_d_dict['day_1_comment'])
                self.assertEqual(sch_d['day_2_start'],
                                 self.sch_d_dict['day_2_start'])
                self.assertEqual(sch_d['day_2_end'],
                                 self.sch_d_dict['day_2_end'])
                self.assertEqual(sch_d['day_2_comment'],
                                 self.sch_d_dict['day_2_comment'])
                self.assertEqual(sch_d['day_3_start'],
                                 self.sch_d_dict['day_3_start'])
                self.assertEqual(sch_d['day_3_end'],
                                 self.sch_d_dict['day_3_end'])
                self.assertEqual(sch_d['day_3_comment'],
                                 self.sch_d_dict['day_3_comment'])
                self.assertEqual(sch_d['day_4_start'],
                                 self.sch_d_dict['day_4_start'])
                self.assertEqual(sch_d['day_4_end'],
                                 self.sch_d_dict['day_4_end'])
                self.assertEqual(sch_d['day_4_comment'],
                                 self.sch_d_dict['day_4_comment'])
                self.assertEqual(sch_d['day_5_start'],
                                 self.sch_d_dict['day_5_start'])
                self.assertEqual(sch_d['day_5_end'],
                                 self.sch_d_dict['day_5_end'])
                self.assertEqual(sch_d['day_5_comment'],
                                 self.sch_d_dict['day_5_comment'])
                self.assertEqual(sch_d['day_6_start'],
                                 self.sch_d_dict['day_6_start'])
                self.assertEqual(sch_d['day_6_end'],
                                 self.sch_d_dict['day_6_end'])
                self.assertEqual(sch_d['day_6_comment'],
                                 self.sch_d_dict['day_6_comment'])
                self.assertEqual(sch_d['day_7_start'],
                                 self.sch_d_dict['day_7_start'])
                self.assertEqual(sch_d['day_7_end'],
                                 self.sch_d_dict['day_7_end'])
                self.assertEqual(sch_d['day_7_comment'],
                                 self.sch_d_dict['day_7_comment'])
                self.assertEqual(sch_d['employee_id'],
                                 self.sch_d_dict['employee_id'])
                self.assertEqual(sch_d['schedule_id'],
                                 self.sch_d_dict['schedule_id'])

    def test_sch_d_get_not_found(self):
        """
        Test that a GET request to the /schedule_detail/<int:detail_id>
        endpoint returns status code 404 if the schedule detail is not
        found in the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/schedule_detail/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_sch_d_get_without_authentication(self):
        """
        Test that a GET request to the /schedule_detail/<int:detail_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/schedule_detail/{self.get_schedule_detail().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_sch_d_put_with_authentication(self):
        """
        Test that a PUT request to the /schedule_detail/<int:detail_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/schedule_detail/{self.get_schedule_detail().id}',
                          data=json.dumps({
                              'day_1_start': '2018-02-01T06:00:00',
                              'day_1_end': '2018-02-01T14:00:00',
                              'day_1_comment': 'comment 1',
                              'day_2_start': '2018-02-02T06:00:00',
                              'day_2_end': '2018-02-02T14:00:00',
                              'day_2_comment': 'comment 2',
                              'day_3_start': '2018-02-03T06:00:00',
                              'day_3_end': '2018-02-03T14:00:00',
                              'day_3_comment': 'comment 3',
                              'day_4_start': '2018-02-04T06:00:00',
                              'day_4_end': '2018-02-04T14:00:00',
                              'day_4_comment': 'comment 4',
                              'day_5_start': None,
                              'day_5_end': None,
                              'day_5_comment': None,
                              'day_6_start': '2018-02-06T22:00:00',
                              'day_6_end': '2018-02-07T06:00:00',
                              'day_6_comment': 'comment 6',
                              'day_7_start': '2018-02-07T22:00:00',
                              'day_7_end': '2018-02-08T06:00:00',
                              'day_7_comment': 'comment 7',
                              'employee_id': self.sch_d_dict['employee_id'],
                              'schedule_id': self.sch_d_dict['schedule_id']
                          }),
                          headers=self.get_headers())

                sch_d = json.loads(r.data)['schedule_detail']

                self.assertEqual(sch_d['day_1_start'],
                                 '2018-02-01T06:00:00')
                self.assertEqual(sch_d['day_1_end'],
                                 '2018-02-01T14:00:00')
                self.assertEqual(sch_d['day_1_comment'],
                                 'comment 1')
                self.assertEqual(sch_d['day_2_start'],
                                 '2018-02-02T06:00:00')
                self.assertEqual(sch_d['day_2_end'],
                                 '2018-02-02T14:00:00')
                self.assertEqual(sch_d['day_2_comment'],
                                 'comment 2')
                self.assertEqual(sch_d['day_3_start'],
                                 '2018-02-03T06:00:00')
                self.assertEqual(sch_d['day_3_end'],
                                 '2018-02-03T14:00:00')
                self.assertEqual(sch_d['day_3_comment'],
                                 'comment 3')
                self.assertEqual(sch_d['day_4_start'],
                                 '2018-02-04T06:00:00')
                self.assertEqual(sch_d['day_4_end'],
                                 '2018-02-04T14:00:00')
                self.assertEqual(sch_d['day_4_comment'],
                                 'comment 4')
                self.assertEqual(sch_d['day_5_start'],
                                 None)
                self.assertEqual(sch_d['day_5_end'],
                                 None)
                self.assertEqual(sch_d['day_5_comment'],
                                 None)
                self.assertEqual(sch_d['day_6_start'],
                                 '2018-02-06T22:00:00')
                self.assertEqual(sch_d['day_6_end'],
                                 '2018-02-07T06:00:00')
                self.assertEqual(sch_d['day_6_comment'],
                                 'comment 6')
                self.assertEqual(sch_d['day_7_start'],
                                 '2018-02-07T22:00:00')
                self.assertEqual(sch_d['day_7_end'],
                                 '2018-02-08T06:00:00')
                self.assertEqual(sch_d['day_7_comment'],
                                 'comment 7')
                self.assertEqual(sch_d['employee_id'],
                                 self.sch_d_dict['employee_id'])
                self.assertEqual(sch_d['schedule_id'],
                                 self.sch_d_dict['schedule_id'])
                self.assertEqual(r.status_code, 200)

    def test_sch_d_put_without_authentication(self):
        """
        Test that a PUT request to the /schedule_detail/<int:detail_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/schedule_detail/{self.get_schedule_detail().id}',
                          data=json.dumps({
                              'day_1_start': '2018-02-01T06:00:00',
                              'day_1_end': '2018-02-01T14:00:00',
                              'day_1_comment': 'comment 1',
                              'day_2_start': '2018-02-02T06:00:00',
                              'day_2_end': '2018-02-02T14:00:00',
                              'day_2_comment': 'comment 2',
                              'day_3_start': '2018-02-03T06:00:00',
                              'day_3_end': '2018-02-03T14:00:00',
                              'day_3_comment': 'comment 3',
                              'day_4_start': '2018-02-04T06:00:00',
                              'day_4_end': '2018-02-04T14:00:00',
                              'day_4_comment': 'comment 4',
                              'day_5_start': None,
                              'day_5_end': None,
                              'day_5_comment': None,
                              'day_6_start': '2018-02-06T22:00:00',
                              'day_6_end': '2018-02-07T06:00:00',
                              'day_6_comment': 'comment 6',
                              'day_7_start': '2018-02-07T22:00:00',
                              'day_7_end': '2018-02-08T06:00:00',
                              'day_7_comment': 'comment 7',
                              'employee_id': self.sch_d_dict['employee_id'],
                              'schedule_id': self.sch_d_dict['schedule_id']
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_sch_d_put_not_found(self):
        """
        Test that a PUT request to the /schedule_detail/<int:detail_id>
        endpoint returns status code 404 if the schedule detail is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/schedule_detail/1',
                          data=json.dumps({
                              'day_1_start': '2018-02-01T06:00:00',
                              'day_1_end': '2018-02-01T14:00:00',
                              'day_1_comment': 'comment 1',
                              'day_2_start': '2018-02-02T06:00:00',
                              'day_2_end': '2018-02-02T14:00:00',
                              'day_2_comment': 'comment 2',
                              'day_3_start': '2018-02-03T06:00:00',
                              'day_3_end': '2018-02-03T14:00:00',
                              'day_3_comment': 'comment 3',
                              'day_4_start': '2018-02-04T06:00:00',
                              'day_4_end': '2018-02-04T14:00:00',
                              'day_4_comment': 'comment 4',
                              'day_5_start': None,
                              'day_5_end': None,
                              'day_5_comment': None,
                              'day_6_start': '2018-02-06T22:00:00',
                              'day_6_end': '2018-02-07T06:00:00',
                              'day_6_comment': 'comment 6',
                              'day_7_start': '2018-02-07T22:00:00',
                              'day_7_end': '2018-02-08T06:00:00',
                              'day_7_comment': 'comment 7',
                              'employee_id': self.sch_d_dict['employee_id'],
                              'schedule_id': self.sch_d_dict['schedule_id']
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_sch_d_delete_with_authentication(self):
        """
        Test that a DELETE request to the /schedule_detail/<int:detail_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/schedule_detail/'
                             f'{self.get_schedule_detail().id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_sch_d_delete_without_authentication(self):
        """
        Test that a DELETE request to the /schedule_detail/<int:detail_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/schedule_detail/{self.get_schedule_detail().id}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_sch_d_delete_not_found(self):
        """
        Test that a DELETE request to the /schedule_detail/<int:detail_id>
        endpoint returns status code 404 if the schedule detail is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/schedule_detail/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
