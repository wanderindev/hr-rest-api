import json

from models.schedule import ScheduleModel
from tests.base_test import BaseTest


class TestSchedule(BaseTest):
    """System tests for the schedule resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a dict representing
        a schedule.
        """
        super(TestSchedule, self).setUp()

        with self.app_context():
            self.sch_dict = {
                'start_date': '2018-01-01',
                'department_id': self.get_department().id,
            }

    def test_sch_post_with_authentication(self):
        """
        Test that a POST request to the /schedule endpoint returns
        status code 201 and that the schedule is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                self.assertIsNone(ScheduleModel.query.filter_by(
                    start_date=self.sch_dict['start_date'],
                    department_id=self.sch_dict['department_id']).first())

                r = c.post('/schedule',
                           data=json.dumps(self.sch_dict),
                           headers=self.get_headers())

                sch = json.loads(r.data)['schedule']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(sch['start_date'],
                                 self.sch_dict['start_date'])
                self.assertEqual(sch['department_id'],
                                 self.sch_dict['department_id'])
                self.assertIsNotNone(ScheduleModel.find_by_id(sch['id'], 
                                                              self.u))

    def test_sch_post_without_authentication(self):
        """
        Test that a POST request to the /schedule endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /schedule endpoint with
                # wrong authentication header.
                r = c.post('/schedule',
                           data=json.dumps(self.sch_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_sch_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicated data to the /schedule endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/schedule',
                       data=json.dumps(self.sch_dict),
                       headers=self.get_headers())

                # Send duplicated POST request.
                r = c.post('/schedule',
                           data=json.dumps(self.sch_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)
                
    def test_sch_post_wrong_user(self):
        """
        Test that status code 403 is returned when trying to POST a
        schedule with a user without permission.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/schedule',
                           data=json.dumps(self.sch_dict),
                           headers=self.get_headers({
                               'username': 'test_other_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 403)

    def test_sch_get_with_authentication(self):
        """
        Test that a GET request to the /schedule/<int:schedule_id>
        endpoint returns the correct schedule and status code 200 if the
        user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/schedule/{self.get_schedule().id}',
                          headers=self.get_headers())

                sch = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(sch['start_date'],
                                 self.sch_dict['start_date'])
                self.assertEqual(sch['department_id'],
                                 self.sch_dict['department_id'])

    def test_sch_get_not_found(self):
        """
        Test that a GET request to the /schedule/<int:schedule_id>
        endpoint returns status code 404 if the schedule is not found in
        the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/schedule/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_sch_get_without_authentication(self):
        """
        Test that a GET request to the /schedule/<int:schedule_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/schedule/{self.get_schedule().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_sch_put_with_authentication(self):
        """
        Test that a PUT request to the /schedule/<int:schedule_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/schedule/{self.get_schedule().id}',
                          data=json.dumps({
                              'start_date': '2018-01-31',
                              'department_id': self.get_department().id
                          }),
                          headers=self.get_headers())

                sch = json.loads(r.data)['schedule']

                self.assertEqual(sch['start_date'],
                                 '2018-01-31')
                self.assertEqual(sch['department_id'],
                                 self.get_department().id)
                self.assertEqual(r.status_code, 200)

    def test_sch_put_without_authentication(self):
        """
        Test that a PUT request to the /schedule/<int:schedule_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/schedule/{self.get_schedule().id}',
                          data=json.dumps({
                              'start_date': '2018-01-31',
                              'department_id': self.get_department().id
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_sch_put_not_found(self):
        """
        Test that a PUT request to the /schedule/<int:schedule_id>
        endpoint returns status code 404 if the schedule is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/schedule/1',
                          data=json.dumps({
                              'start_date': '2018-01-31',
                              'department_id': self.get_department().id
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_sch_delete_with_authentication(self):
        """
        Test that a DELETE request to the /schedule/<int:schedule_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/schedule/{self.get_schedule().id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_sch_delete_without_authentication(self):
        """
        Test that a DELETE request to the /schedule/<int:schedule_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/schedule/{self.get_schedule().id}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_sch_delete_not_found(self):
        """
        Test that a DELETE request to the /schedule/<int:schedule_id>
        endpoint returns status code 404 if the schedule is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/schedule/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
