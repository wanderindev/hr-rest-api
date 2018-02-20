import json

from models.bank_account import BankAccountModel
from tests.base_test import BaseTest


class TestBankAccount(BaseTest):
    """System tests for the bank_account resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a department, an
        employment_position, a shift, an employee, and a dict representing
        a bank_account..
        """
        super(TestBankAccount, self).setUp()

        with self.app_context():
            self.d = self.get_department(1)
            self.e_p = self.get_employment_position(1)
            self.s = self.get_shift(1)
            self.e = self.get_employee(self.d.id, self.e_p.id, self.s.id, 1)
            self.b_a_dict = {
                'account_number': '1234',
                'account_type': 'Corriente',
                'is_active': True,
                'employee_id': self.e.id,
                'bank_id': 1
            }

    def test_b_acc_post_with_authentication(self):
        """
        Test that a POST request to the /bank_account endpoint returns
        status code 201 and that the bank_account is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                self.assertIsNone(BankAccountModel.query.filter_by(
                    account_number=self.b_a_dict['account_number']).first())

                r = c.post('/bank_account',
                           data=json.dumps(self.b_a_dict),
                           headers=self.get_headers())

                r_b_a = json.loads(r.data)['bank_account']

                self.assertEqual(r.status_code, 201)
                self.assertTrue(r_b_a['is_active'])
                self.assertEqual(r_b_a['account_number'],
                                 self.b_a_dict['account_number'])
                self.assertEqual(r_b_a['account_type'],
                                 self.b_a_dict['account_type'])
                self.assertEqual(r_b_a['employee_id'],
                                 self.b_a_dict['employee_id'])
                self.assertEqual(r_b_a['bank_id'],
                                 self.b_a_dict['bank_id'])
                self.assertIsNotNone(BankAccountModel.find_by_id(
                    r_b_a['id'],
                    self.d.organization_id))

    def test_b_acc_post_without_authentication(self):
        """
        Test that a POST request to the /bank_account endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /bank_account endpoint with
                # wrong authentication header.
                r = c.post('/bank_account',
                           data=json.dumps(self.b_a_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_b_acc_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicated data to the /bank_account endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/bank_account',
                       data=json.dumps(self.b_a_dict),
                       headers=self.get_headers())

                # Send duplicated POST request.
                r = c.post('/bank_account',
                           data=json.dumps(self.b_a_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_b_acc_get_with_authentication(self):
        """
        Test that a GET request to the /bank_account/<int:account_id>
        endpoint returns the correct bank_account and status code 200 if the
        user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/bank_account',
                           data=json.dumps(self.b_a_dict),
                           headers=self.get_headers())

                account_id = json.loads(r.data)['bank_account']['id']

                r = c.get(f'/bank_account/{account_id}',
                          headers=self.get_headers())

                r_dict = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(r_dict['account_number'],
                                 self.b_a_dict['account_number'])
                self.assertEqual(r_dict['account_type'],
                                 self.b_a_dict['account_type'])
                self.assertEqual(r_dict['employee_id'],
                                 self.b_a_dict['employee_id'])
                self.assertEqual(r_dict['bank_id'],
                                 self.b_a_dict['bank_id'])
                self.assertTrue(r_dict['is_active'])

    def test_b_acc_get_not_found(self):
        """
        Test that a GET request to the /bank_account/<int:account_id>
        endpoint returns status code 404 if the bank_account is not found in
        the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/bank_account/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_b_acc_get_without_authentication(self):
        """
        Test that a GET request to the /bank_account/<int:account_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/bank_account/1',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_b_acc_put_with_authentication(self):
        """
        Test that a PUT request to the /bank_account/<int:account_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/bank_account',
                           data=json.dumps(self.b_a_dict),
                           headers=self.get_headers())

                account_id = json.loads(r.data)['bank_account']['id']

                r = c.put(f'/bank_account/{account_id}',
                          data=json.dumps({
                              'account_number': '4321',
                              'account_type': 'Ahorro',
                              'is_active': True,
                              'employee_id': self.e.id,
                              'bank_id': 2,
                          }),
                          headers=self.get_headers())

                r_b_a = json.loads(r.data)['bank_account']

                self.assertTrue(r_b_a['is_active'])
                self.assertEqual(r_b_a['account_number'],
                                 '4321')
                self.assertEqual(r_b_a['account_type'],
                                 'Ahorro')
                self.assertEqual(r_b_a['employee_id'],
                                 self.e.id)
                self.assertEqual(r_b_a['bank_id'],
                                 2)
                self.assertEqual(r.status_code, 200)

    def test_b_acc_put_without_authentication(self):
        """
        Test that a PUT request to the /bank_account/<int:account_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/bank_account/1',
                          data=json.dumps({
                              'account_number': '4321',
                              'account_type': 'Ahorro',
                              'is_active': True,
                              'employee_id': self.e.id,
                              'bank_id': 2,
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_b_acc_put_not_found(self):
        """
        Test that a PUT request to the /bank_account/<int:account_id>
        endpoint returns status code 404 if the bank_account is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/bank_account/1',
                          data=json.dumps({
                              'account_number': '4321',
                              'account_type': 'Ahorro',
                              'is_active': True,
                              'employee_id': self.e.id,
                              'bank_id': 2,
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_b_acc_delete_with_authentication(self):
        """
        Test that a DELETE request to the /bank_account/<int:account_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/bank_account',
                           data=json.dumps(self.b_a_dict),
                           headers=self.get_headers())

                account_id = json.loads(r.data)['bank_account']['id']

                r = c.delete(f'/bank_account/{account_id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_b_acc_delete_without_authentication(self):
        """
        Test that a DELETE request to the /bank_account/<int:account_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/bank_account/1',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_b_acc_delete_inactive(self):
        """
        Test that a DELETE request to the /bank_account/<int:account_id>
        endpoint returns status code 400 if the bank_account is already
        inactive.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/bank_account',
                           data=json.dumps(self.b_a_dict),
                           headers=self.get_headers())

                account_id = json.loads(r.data)['bank_account']['id']

                # Make bank_account inactive.
                c.delete(f'/bank_account/{account_id}',
                         headers=self.get_headers())

                # Send DELETE request on inactive bank_account.
                r = c.delete(f'/bank_account/{account_id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_b_acc_delete_not_found(self):
        """
        Test that a DELETE request to the /bank_account/<int:account_id>
        endpoint returns status code 404 if the bank_account is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/bank_account/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_activate_b_acc_with_authentication(self):
        """
        Test that a PUT request to the /activate_bank_account
        /<int:account_id> endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/bank_account',
                           data=json.dumps(self.b_a_dict),
                           headers=self.get_headers())

                account_id = json.loads(r.data)['bank_account']['id']

                c.delete(f'/bank_account/{account_id}',
                         headers=self.get_headers())

                r = c.put(f'/activate_bank_account/'
                          f'{account_id}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_activate_b_acc_without_authentication(self):
        """
        Test that a PUT request to the /activate_bank_account
        /<int:account_id> endpoint returns status code
        401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_bank_account with
                # wrong authorization header.
                r = c.put(f'/activate_bank_account/1',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_activate_b_acc_active(self):
        """
        Test that a PUT request to the /activate_bank_account
        /<int:account_id>_name endpoint returns status code 400
        if the bank_account is already active.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/bank_account',
                           data=json.dumps(self.b_a_dict),
                           headers=self.get_headers())

                account_id = json.loads(r.data)['bank_account']['id']

                r = c.put(f'/activate_bank_account/{account_id}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_activate_b_acc_not_found(self):
        """
        Test that a PUT request to the /activate_bank_account
        /<int:account_id> endpoint returns status code
        404 if the bank_account is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_bank_account/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
