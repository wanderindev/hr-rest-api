import json

from models.payment import PaymentModel
from tests.base_test import BaseTest


class TestPayment(BaseTest):
    """System tests for the payment resource."""

    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a
        dict representing an payment.
        """
        super(TestPayment, self).setUp()

        with self.app_context():
            self.pmt_dict = {
                'payment_date': '2018-01-01',
                'document_number': '1234-abc',
                'employee_id': self.get_employee().id
            }

    def test_pmt_post_with_authentication(self):
        """
        Test that a POST request to the /payment endpoint returns
        status code 201 and that the payment is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/payment',
                           data=json.dumps(self.pmt_dict),
                           headers=self.get_headers())

                pmt = json.loads(r.data)['payment']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(pmt['payment_date'],
                                 self.pmt_dict['payment_date'])
                self.assertEqual(pmt['document_number'],
                                 self.pmt_dict['document_number'])
                self.assertEqual(pmt['employee_id'],
                                 self.pmt_dict['employee_id'])
                self.assertIsNotNone(PaymentModel.find_by_id(pmt['id'],
                                                             self.u))

    def test_pmt_post_without_authentication(self):
        """
        Test that a POST request to the /payment endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /payment endpoint with
                # wrong authentication header.
                r = c.post('/payment',
                           data=json.dumps(self.pmt_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_pmt_post_wrong_user(self):
        """
        Test that status code 403 is returned when trying to POST an
        payment with a user without permission.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/payment',
                           data=json.dumps(self.pmt_dict),
                           headers=self.get_headers({
                               'username': 'test_other_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 403)

    def test_pmt_get_with_authentication(self):
        """
        Test that a GET request to the /payment/<int:payment_id>
        endpoint returns the correct payment and status code 200 if
        the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/payment/{self.get_payment().id}',
                          headers=self.get_headers())

                pmt = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(pmt['payment_date'],
                                 self.pmt_dict['payment_date'])
                self.assertEqual(pmt['document_number'],
                                 self.pmt_dict['document_number'])
                self.assertEqual(pmt['employee_id'],
                                 self.pmt_dict['employee_id'])

    def test_pmt_get_not_found(self):
        """
        Test that a GET request to the /payment/<int:payment_id>
        endpoint returns status code 404 if the payment is not
        found in the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/payment/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_pmt_get_without_authentication(self):
        """
        Test that a GET request to the /payment/<int:payment_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/payment/{self.get_payment().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_pmt_put_with_authentication(self):
        """
        Test that a PUT request to the /payment/<int:payment_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/payment/{self.get_payment().id}',
                          data=json.dumps({
                              'payment_date': '2018-02-01',
                              'document_number': '1234-def',
                              'employee_id': self.get_employee().id
                          }),
                          headers=self.get_headers())

                pmt = json.loads(r.data)['payment']

                self.assertEqual(pmt['payment_date'], '2018-02-01')
                self.assertEqual(pmt['document_number'], '1234-def')
                self.assertEqual(pmt['employee_id'],
                                 self.pmt_dict['employee_id'])
                self.assertEqual(r.status_code, 200)

    def test_pmt_put_without_authentication(self):
        """
        Test that a PUT request to the /payment/<int:payment_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/payment/{self.get_payment().id}',
                          data=json.dumps({
                              'payment_date': '2018-02-01',
                              'document_number': '1234-def',
                              'employee_id': self.get_employee().id
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_pmt_put_not_found(self):
        """
        Test that a PUT request to the /payment/<int:payment_id>
        endpoint returns status code 404 if the payment is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/payment/1',
                          data=json.dumps({
                              'payment_date': '2018-02-01',
                              'document_number': '1234-def',
                              'employee_id': self.get_employee().id
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_pmt_delete_with_authentication(self):
        """
        Test that a DELETE request to the /payment/<int:payment_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/payment/{self.get_payment().id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_pmt_delete_without_authentication(self):
        """
        Test that a DELETE request to the /payment/<int:payment_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/payment/{self.get_payment().id}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_pmt_delete_not_found(self):
        """
        Test that a DELETE request to the /payment/<int:payment_id>
        endpoint returns status code 404 if the payment is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/payment/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
