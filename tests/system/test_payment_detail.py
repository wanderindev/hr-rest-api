import json

from models.payment_detail import PaymentDetailModel
from tests.base_test import BaseTest


class TestPaymentDetail(BaseTest):
    """System tests for the payment_detail resource."""

    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a
        dict representing a payment_detail.
        """
        super(TestPaymentDetail, self).setUp()

        with self.app_context():
            self.pmt_d_dict = {
                'payment_type': 'Salario Regular',
                'gross_payment': 1234.56,
                'ss_deduction': 123.45,
                'se_deduction': 12.34,
                'isr_deduction': 1.23,
                'payment_id': self.get_payment().id
            }

    def test_pmt_d_post_with_authentication(self):
        """
        Test that a POST request to the /payment_detail endpoint returns
        status code 201 and that the payment_detail is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/payment_detail',
                           data=json.dumps(self.pmt_d_dict),
                           headers=self.get_headers())

                pmt_d = json.loads(r.data)['payment_detail']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(pmt_d['payment_type'],
                                 self.pmt_d_dict['payment_type'])
                self.assertEqual(float(pmt_d['gross_payment']),
                                 self.pmt_d_dict['gross_payment'])
                self.assertEqual(float(pmt_d['ss_deduction']),
                                 self.pmt_d_dict['ss_deduction'])
                self.assertEqual(float(pmt_d['se_deduction']),
                                 self.pmt_d_dict['se_deduction'])
                self.assertEqual(float(pmt_d['isr_deduction']),
                                 self.pmt_d_dict['isr_deduction'])
                self.assertEqual(pmt_d['payment_id'],
                                 self.pmt_d_dict['payment_id'])
                self.assertIsNotNone(PaymentDetailModel.find_by_id(pmt_d['id'],
                                                                   self.u))

    def test_pmt_d_post_without_authentication(self):
        """
        Test that a POST request to the /payment_detail endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /payment_detail endpoint with
                # wrong authentication header.
                r = c.post('/payment_detail',
                           data=json.dumps(self.pmt_d_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_pmt_d_post_wrong_user(self):
        """
        Test that status code 403 is returned when trying to POST an
        payment_detail with a user without permission.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/payment_detail',
                           data=json.dumps(self.pmt_d_dict),
                           headers=self.get_headers({
                               'username': 'test_other_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 403)

    def test_pmt_d_get_with_authentication(self):
        """
        Test that a GET request to the /payment_detail/<int:detail_id>
        endpoint returns the correct payment_detail and status code 200 if
        the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/payment_detail/{self.get_payment_detail().id}',
                          headers=self.get_headers())

                pmt_d = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(pmt_d['payment_type'],
                                 self.pmt_d_dict['payment_type'])
                self.assertEqual(float(pmt_d['gross_payment']),
                                 self.pmt_d_dict['gross_payment'])
                self.assertEqual(float(pmt_d['ss_deduction']),
                                 self.pmt_d_dict['ss_deduction'])
                self.assertEqual(float(pmt_d['se_deduction']),
                                 self.pmt_d_dict['se_deduction'])
                self.assertEqual(float(pmt_d['isr_deduction']),
                                 self.pmt_d_dict['isr_deduction'])
                self.assertEqual(pmt_d['payment_id'],
                                 self.pmt_d_dict['payment_id'])

    def test_pmt_d_get_not_found(self):
        """
        Test that a GET request to the /payment_detail/<int:detail_id>
        endpoint returns status code 404 if the payment_detail is not
        found in the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/payment_detail/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_pmt_d_get_without_authentication(self):
        """
        Test that a GET request to the /payment_detail/<int:detail_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/payment_detail/{self.get_payment_detail().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_pmt_d_put_with_authentication(self):
        """
        Test that a PUT request to the /payment_detail/<int:detail_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/payment_detail/{self.get_payment_detail().id}',
                          data=json.dumps({
                              'payment_type': 'Vacación',
                              'gross_payment': 2345.67,
                              'ss_deduction': 234.56,
                              'se_deduction': 23.45,
                              'isr_deduction': 2.34,
                              'payment_id': self.get_payment().id
                          }),
                          headers=self.get_headers())

                pmt_d = json.loads(r.data)['payment_detail']

                self.assertEqual(pmt_d['payment_type'], 'Vacación')
                self.assertEqual(float(pmt_d['gross_payment']), 2345.67)
                self.assertEqual(float(pmt_d['ss_deduction']), 234.56)
                self.assertEqual(float(pmt_d['se_deduction']), 23.45)
                self.assertEqual(float(pmt_d['isr_deduction']), 2.34)
                self.assertEqual(pmt_d['payment_id'], self.get_payment().id)
                self.assertEqual(r.status_code, 200)

    def test_pmt_d_put_without_authentication(self):
        """
        Test that a PUT request to the /payment_detail/<int:detail_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/payment_detail/{self.get_payment_detail().id}',
                          data=json.dumps({
                              'payment_type': 'Vacación',
                              'gross_payment': 2345.67,
                              'ss_deduction': 234.56,
                              'se_deduction': 23.45,
                              'isr_deduction': 2.34,
                              'payment_id': self.get_payment().id
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_pmt_d_put_not_found(self):
        """
        Test that a PUT request to the /payment_detail/<int:detail_id>
        endpoint returns status code 404 if the payment_detail is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/payment_detail/1',
                          data=json.dumps({
                              'payment_type': 'Vacación',
                              'gross_payment': 2345.67,
                              'ss_deduction': 234.56,
                              'se_deduction': 23.45,
                              'isr_deduction': 2.34,
                              'payment_id': self.get_payment().id
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_pmt_d_delete_with_authentication(self):
        """
        Test that a DELETE request to the /payment_detail/<int:detail_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/payment_detail/{self.get_payment_detail().id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_pmt_d_delete_without_authentication(self):
        """
        Test that a DELETE request to the /payment_detail/<int:detail_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/payment_detail/{self.get_payment_detail().id}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_pmt_d_delete_not_found(self):
        """
        Test that a DELETE request to the /payment_detail/<int:detail_id>
        endpoint returns status code 404 if the payment_detail is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/payment_detail/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
