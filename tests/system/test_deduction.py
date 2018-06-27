import json

from models.deduction import DeductionModel
from tests.base_test import BaseTest


class TestDeduction(BaseTest):
    """System tests for the deduction resource."""

    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a
        dict representing an deduction.
        """
        super(TestDeduction, self).setUp()

        with self.app_context():
            self.ded_dict = {
                'start_date': '2018-01-01',
                'end_date': '2018-01-31',
                'deduction_per_payment_period': 123.45,
                'payment_method': 'Cheque',
                'deduct_in_december': True,
                'is_active': True,
                'employee_id': self.get_employee().id,
                'creditor_id': self.get_creditor().id
            }

    def test_ded_post_with_authentication(self):
        """
        Test that a POST request to the /deduction endpoint returns
        status code 201 and that the deduction is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/deduction',
                           data=json.dumps(self.ded_dict),
                           headers=self.get_headers())

                ded = json.loads(r.data)['deduction']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(ded['start_date'],
                                 self.ded_dict['start_date'])
                self.assertEqual(ded['end_date'],
                                 self.ded_dict['end_date'])
                self.assertEqual(float(ded['deduction_per_payment_period']),
                                 self.ded_dict['deduction_per_payment_period'])
                self.assertEqual(ded['payment_method'],
                                 self.ded_dict['payment_method'])
                self.assertEqual(ded['deduct_in_december'],
                                 self.ded_dict['deduct_in_december'])
                self.assertEqual(ded['is_active'],
                                 self.ded_dict['is_active'])
                self.assertEqual(ded['employee_id'],
                                 self.ded_dict['employee_id'])
                self.assertEqual(ded['creditor_id'],
                                 self.ded_dict['creditor_id'])
                self.assertIsNotNone(DeductionModel.find_by_id(ded['id'],
                                                               self.u))

    def test_ded_post_without_authentication(self):
        """
        Test that a POST request to the /deduction endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /deduction endpoint with
                # wrong authentication header.
                r = c.post('/deduction',
                           data=json.dumps(self.ded_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_ded_post_wrong_user(self):
        """
        Test that status code 403 is returned when trying to POST an
        deduction with a user without permission.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/deduction',
                           data=json.dumps(self.ded_dict),
                           headers=self.get_headers({
                               'username': 'test_other_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 403)

    def test_ded_get_with_authentication(self):
        """
        Test that a GET request to the /deduction/<int:deduction_id>
        endpoint returns the correct deduction and status code 200 if
        the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/deduction/{self.get_deduction().id}',
                          headers=self.get_headers())

                ded = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(ded['start_date'],
                                 self.ded_dict['start_date'])
                self.assertEqual(ded['end_date'],
                                 self.ded_dict['end_date'])
                self.assertEqual(float(ded['deduction_per_payment_period']),
                                 self.ded_dict['deduction_per_payment_period'])
                self.assertEqual(ded['payment_method'],
                                 self.ded_dict['payment_method'])
                self.assertEqual(ded['deduct_in_december'],
                                 self.ded_dict['deduct_in_december'])
                self.assertEqual(ded['is_active'],
                                 self.ded_dict['is_active'])
                self.assertEqual(ded['employee_id'],
                                 self.ded_dict['employee_id'])
                self.assertEqual(ded['creditor_id'],
                                 self.ded_dict['creditor_id'])

    def test_ded_get_not_found(self):
        """
        Test that a GET request to the /deduction/<int:deduction_id>
        endpoint returns status code 404 if the deduction is not
        found in the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/deduction/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_ded_get_without_authentication(self):
        """
        Test that a GET request to the /deduction/<int:deduction_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/deduction/{self.get_deduction().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_ded_put_with_authentication(self):
        """
        Test that a PUT request to the /deduction/<int:deduction_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/deduction/{self.get_deduction().id}',
                          data=json.dumps({
                              'start_date': '2018-02-01',
                              'end_date': '2018-02-28',
                              'deduction_per_payment_period': 45.67,
                              'payment_method': 'Efectivo',
                              'deduct_in_december': False,
                              'is_active': True,
                              'employee_id': self.get_organization().id,
                              'creditor_id': self.get_creditor().id
                            }),
                          headers=self.get_headers())

                ded = json.loads(r.data)['deduction']

                self.assertEqual(ded['start_date'], '2018-02-01')
                self.assertEqual(ded['end_date'], '2018-02-31')
                self.assertEqual(float(ded['deduction_per_payment_period']),
                                 45.67)
                self.assertEqual(ded['payment_method'], 'Efectivo')
                self.assertEqual(ded['deduct_in_december'], False)
                self.assertEqual(ded['is_active'], True)
                self.assertEqual(ded['employee_id'],
                                 self.ded_dict['employee_id'])
                self.assertEqual(ded['creditor_id'],
                                 self.ded_dict['creditor_id'])
                self.assertEqual(r.status_code, 200)

    def test_ded_put_without_authentication(self):
        """
        Test that a PUT request to the /deduction/<int:deduction_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/deduction/{self.get_deduction().id}',
                          data=json.dumps({
                              'start_date': '2018-02-01',
                              'end_date': '2018-02-31',
                              'deduction_per_payment_period': 45.67,
                              'payment_method': 'Efectivo',
                              'deduct_in_december': False,
                              'is_active': True,
                              'employee_id': self.get_organization().id,
                              'creditor_id': self.get_creditor().id
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_ded_put_not_found(self):
        """
        Test that a PUT request to the /deduction/<int:deduction_id>
        endpoint returns status code 404 if the deduction is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/deduction/1',
                          data=json.dumps({
                              'start_date': '2018-02-01',
                              'end_date': '2018-02-31',
                              'deduction_per_payment_period': 45.67,
                              'payment_method': 'Efectivo',
                              'deduct_in_december': False,
                              'is_active': True,
                              'employee_id': self.get_organization().id,
                              'creditor_id': self.get_creditor().id
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_ded_delete_with_authentication(self):
        """
        Test that a DELETE request to the /deduction/<int:deduction_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/deduction/{self.get_deduction().id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_ded_delete_without_authentication(self):
        """
        Test that a DELETE request to the /deduction/<int:deduction_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/deduction/{self.get_deduction().id}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_ded_delete_not_found(self):
        """
        Test that a DELETE request to the /deduction/<int:deduction_id>
        endpoint returns status code 404 if the deduction is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/deduction/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_ded_delete_inactive(self):
        """
        Test that a DELETE request to the /deduction/<int:deduction_id>
        endpoint returns status code 400 if the deduction is already inactive.
        """
        with self.app() as c:
            with self.app_context():
                deduction_id = self.get_deduction().id

                # Make deduction inactive.
                c.delete(f'/deduction/{deduction_id}',
                         headers=self.get_headers())

                # Send DELETE request on inactive deduction.
                r = c.delete(f'/deduction/{deduction_id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_activate_ded_with_authentication(self):
        """
        Test that a PUT request to the /activate_deduction/<int:deduction_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                deduction_id = self.get_deduction().id

                c.delete(f'/deduction/{deduction_id}',
                         headers=self.get_headers())

                r = c.put(f'/activate_deduction/{deduction_id}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_activate_ded_without_authentication(self):
        """
        Test that a PUT request to the /activate_deduction/<int:deduction_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_deduction with
                # wrong authorization header.
                r = c.put(f'/activate_deduction/{self.get_deduction().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_activate_ded_active(self):
        """
        Test that a PUT request to the /activate_deduction/<int:deduction_id>
        endpoint returns status code 400 if the deduction is already active.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_deduction/{self.get_deduction().id}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_activate_ded_not_found(self):
        """
        Test that a PUT request to the /activate_deduction/<int:deduction_id>
        endpoint returns status code 404 if the deduction is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_deduction/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
