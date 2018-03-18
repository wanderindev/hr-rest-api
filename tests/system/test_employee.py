import json

from models.employee import EmployeeModel
from tests.base_test import BaseTest


class TestEmployee(BaseTest):
    """System tests for the employee resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a dict
        representing an employee.
        """
        super(TestEmployee, self).setUp()

        with self.app_context():
            self.e_dict = {
                'first_name': 'f_n',
                'second_name': 's_n',
                'first_surname': 'f_sn',
                'second_surname': 's_sn',
                'national_id_number': '1-11-111',
                'is_panamanian': True,
                'date_of_birth': '2000-01-31',
                'gender': 'Hombre',
                'address': 'Panamá',
                'home_phone': '222-2222',
                'mobile_phone': '6666-6666',
                'email': 'f_n@f_sn.com',
                'type_of_contract': 'Definido',
                'employment_date': '2018-01-01',
                'contract_expiration_date': '2018-01-31',
                'termination_date': '2018-01-15',
                'termination_reason': 'Período de Prueba',
                'salary_per_payment_period': 104,
                'representation_expenses_per_payment_period': 0,
                'payment_method': 'ACH',
                'is_active': True,
                'marital_status_id': 1,
                'department_id': self.get_department().id,
                'position_id': self.get_employment_position().id,
                'shift_id': self.get_shift().id
            }

    def test_empl_post_with_authentication(self):
        """
        Test that a POST request to the /employee endpoint returns
        status code 201 and that the employee is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                self.assertIsNone(EmployeeModel.query.filter_by(
                    first_name=self.e_dict['first_name']).first())

                r = c.post('/employee',
                           data=json.dumps(self.e_dict),
                           headers=self.get_headers())

                empl = json.loads(r.data)['employee']

                self.assertEqual(r.status_code, 201)
                self.assertTrue(empl['is_active'])
                self.assertTrue(empl['is_panamanian'])
                self.assertEqual(empl['first_name'], self.e_dict['first_name'])
                self.assertEqual(empl['second_name'],
                                 self.e_dict['second_name'])
                self.assertEqual(empl['first_surname'],
                                 self.e_dict['first_surname'])
                self.assertEqual(empl['second_surname'],
                                 self.e_dict['second_surname'])
                self.assertEqual(empl['gender'], self.e_dict['gender'])
                self.assertEqual(empl['national_id_number'],
                                 self.e_dict['national_id_number'])
                self.assertEqual(empl['date_of_birth'],
                                 self.e_dict['date_of_birth'])
                self.assertEqual(empl['address'], self.e_dict['address'])
                self.assertEqual(empl['home_phone'], self.e_dict['home_phone'])
                self.assertEqual(empl['mobile_phone'],
                                 self.e_dict['mobile_phone'])
                self.assertEqual(empl['email'], self.e_dict['email'])
                self.assertEqual(empl['type_of_contract'],
                                 self.e_dict['type_of_contract'])
                self.assertEqual(empl['payment_method'],
                                 self.e_dict['payment_method'])
                self.assertEqual(float(empl['salary_per_payment_period']),
                                 self.e_dict['salary_per_payment_period'])
                self.assertEqual(
                    float(empl['representation_expenses_per_payment_period']),
                    self.e_dict['representation_expenses_per_payment_period'])
                self.assertEqual(empl['employment_date'],
                                 self.e_dict['employment_date'])
                self.assertEqual(empl['contract_expiration_date'],
                                 self.e_dict['contract_expiration_date'])
                self.assertEqual(empl['termination_date'],
                                 self.e_dict['termination_date'])
                self.assertEqual(empl['termination_reason'],
                                 self.e_dict['termination_reason'])
                self.assertEqual(empl['position_id'],
                                 self.e_dict['position_id'])
                self.assertEqual(empl['department_id'],
                                 self.e_dict['department_id'])
                self.assertEqual(empl['marital_status_id'],
                                 self.e_dict['marital_status_id'])
                self.assertEqual(empl['shift_id'],
                                 self.e_dict['shift_id'])
                self.assertIsNotNone(EmployeeModel.find_by_id(empl['id'],
                                                              self.u))

    def test_empl_post_without_authentication(self):
        """
        Test that a POST request to the /employee endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /employee endpoint with
                # wrong authentication header.
                r = c.post('/employee',
                           data=json.dumps(self.e_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_empl_post_wrong_user(self):
        """
        Test that status code 403 is returned when trying to POST an
        employee with a user without permission.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/employee',
                           data=json.dumps(self.e_dict),
                           headers=self.get_headers({
                               'username': 'test_other_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 403)

    def test_empl_get_with_authentication(self):
        """
        Test that a GET request to the /employee/<int:employee_id>
        endpoint returns the correct employee and status code 200 if the
        user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                employee_id = self.get_employee().id

                r = c.get(f'/employee/{employee_id}',
                          headers=self.get_headers())

                e = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(e['id'], employee_id)

    def test_empl_get_not_found(self):
        """
        Test that a GET request to the /employee/<int:employee_id>
        endpoint returns status code 404 if the employee is not found in
        the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/employee/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_empl_get_without_authentication(self):
        """
        Test that a GET request to the /employee/<int:employee_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/employee/{self.get_employee().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_empl_put_with_authentication(self):
        """
        Test that a PUT request to the /employee/<int:employee_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/employee/{self.get_employee().id}',
                          data=json.dumps({
                              'first_name': 'new_f_n',
                              'second_name': 'new_s_n',
                              'first_surname': 'new_f_sn',
                              'second_surname': 'new_s_sn',
                              'national_id_number': 'N-1-11-111',
                              'is_panamanian': False,
                              'date_of_birth': '01-31-2001',
                              'gender': 'Mujer',
                              'address': 'Chiriquí',
                              'home_phone': '333-3333',
                              'mobile_phone': '6666-7777',
                              'email': 'new_f_n@new_f_sn.com',
                              'type_of_contract': 'Indefinido',
                              'employment_date': '01-01-2019',
                              'contract_expiration_date': '01-31-2019',
                              'termination_date': '01-15-2019',
                              'termination_reason': 'Renuncia',
                              'salary_per_payment_period': '208.00',
                              'representation_expenses_per_payment_period':
                                  '100',
                              'payment_method': 'Cheque',
                              'is_active': True,
                              'marital_status_id': 2,
                              'department_id': self.get_department().id,
                              'position_id': self.get_employment_position().id,
                              'shift_id': self.get_shift().id
                          }),
                          headers=self.get_headers())

                empl = json.loads(r.data)['employee']

                self.assertTrue(empl['is_active'])
                self.assertFalse(empl['is_panamanian'])
                self.assertEqual(empl['first_name'], 'new_f_n')
                self.assertEqual(empl['second_name'], 'new_s_n')
                self.assertEqual(empl['first_surname'], 'new_f_sn')
                self.assertEqual(empl['second_surname'], 'new_s_sn')
                self.assertEqual(empl['gender'], 'Mujer')
                self.assertEqual(empl['national_id_number'], 'N-1-11-111')
                self.assertEqual(empl['date_of_birth'], '2001-01-31')
                self.assertEqual(empl['address'], 'Chiriquí')
                self.assertEqual(empl['home_phone'], '333-3333')
                self.assertEqual(empl['mobile_phone'], '6666-7777')
                self.assertEqual(empl['email'], 'new_f_n@new_f_sn.com')
                self.assertEqual(empl['type_of_contract'], 'Indefinido')
                self.assertEqual(empl['payment_method'], 'Cheque')
                self.assertEqual(float(empl['salary_per_payment_period']), 208)
                self.assertEqual(float(
                    empl['representation_expenses_per_payment_period']), 100)
                self.assertEqual(empl['employment_date'], '2019-01-01')
                self.assertEqual(empl['contract_expiration_date'], '2019-01-31')
                self.assertEqual(empl['termination_date'], '2019-01-15')
                self.assertEqual(empl['termination_reason'], 'Renuncia')
                self.assertEqual(empl['position_id'],
                                 self.get_employment_position().id)
                self.assertEqual(empl['department_id'],
                                 self.get_department().id)
                self.assertEqual(empl['marital_status_id'],  2)
                self.assertEqual(empl['shift_id'], self.get_shift().id)
                self.assertEqual(r.status_code, 200)

    def test_empl_put_without_authentication(self):
        """
        Test that a PUT request to the /employee/<int:employee_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/employee/{self.get_employee().id}',
                          data=json.dumps({
                              'first_name': 'new_f_n',
                              'second_name': 'new_s_n',
                              'first_surname': 'new_f_sn',
                              'second_surname': 'new_s_sn',
                              'national_id_number': 'N-1-11-111',
                              'is_panamanian': False,
                              'date_of_birth': '01-31-2001',
                              'gender': 'Mujer',
                              'address': 'Chiriquí',
                              'home_phone': '333-3333',
                              'mobile_phone': '6666-7777',
                              'email': 'new_f_n@new_f_sn.com',
                              'type_of_contract': 'Indefinido',
                              'employment_date': '01-01-2019',
                              'contract_expiration_date': '01-31-2019',
                              'termination_date': '01-15-2019',
                              'termination_reason': 'Renuncia',
                              'salary_per_payment_period': '208.00',
                              'representation_expenses_per_payment_period':
                                  '100',
                              'payment_method': 'Cheque',
                              'is_active': True,
                              'marital_status_id': 2,
                              'department_id': self.get_department().id,
                              'position_id': self.get_employment_position().id,
                              'shift_id': self.get_shift().id
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_empl_put_not_found(self):
        """
        Test that a PUT request to the /employee/<int:employee_id>
        endpoint returns status code 404 if the employee is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/employee/1',
                          data=json.dumps({
                              'first_name': 'new_f_n',
                              'second_name': 'new_s_n',
                              'first_surname': 'new_f_sn',
                              'second_surname': 'new_s_sn',
                              'national_id_number': 'N-1-11-111',
                              'is_panamanian': False,
                              'date_of_birth': '01-31-2001',
                              'gender': 'Mujer',
                              'address': 'Chiriquí',
                              'home_phone': '333-3333',
                              'mobile_phone': '6666-7777',
                              'email': 'new_f_n@new_f_sn.com',
                              'type_of_contract': 'Indefinido',
                              'employment_date': '01-01-2019',
                              'contract_expiration_date': '01-31-2019',
                              'termination_date': '01-15-2019',
                              'termination_reason': 'Renuncia',
                              'salary_per_payment_period': '208.00',
                              'representation_expenses_per_payment_period':
                                  '100',
                              'payment_method': 'Cheque',
                              'is_active': True,
                              'marital_status_id': 2,
                              'department_id': self.get_department().id,
                              'position_id': self.get_employment_position().id,
                              'shift_id': self.get_shift().id
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_empl_delete_with_authentication(self):
        """
        Test that a DELETE request to the /employee/<int:employee_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/employee/{self.get_employee().id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_empl_delete_without_authentication(self):
        """
        Test that a DELETE request to the /employee/<int:employee_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/employee/{self.get_employee().id}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_empl_delete_inactive(self):
        """
        Test that a DELETE request to the /employee/<int:employee_id>
        endpoint returns status code 400 if the employee is already inactive.
        """
        with self.app() as c:
            with self.app_context():
                employee_id = self.get_employee().id

                # Make employee inactive.
                c.delete(f'/employee/{employee_id}',
                         headers=self.get_headers())

                # Send DELETE request on inactive employee.
                r = c.delete(f'/employee/{employee_id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_empl_delete_not_found(self):
        """
        Test that a DELETE request to the /employee/<int:employee_id>
        endpoint returns status code 404 if the employee is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/employee/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_activate_empl_with_authentication(self):
        """
        Test that a PUT request to the /activate_employee
        /<int:employee_id> endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                employee_id = self.get_employee().id

                c.delete(f'/employee/{employee_id}',
                         headers=self.get_headers())

                r = c.put(f'/activate_employee/{employee_id}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_activate_empl_without_authentication(self):
        """
        Test that a PUT request to the /activate_employee
        /<int:employee_id> endpoint returns status code
        401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_employee with
                # wrong authorization header.
                r = c.put(f'/activate_employee/'
                          f'{self.get_employee().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_activate_empl_active(self):
        """
        Test that a PUT request to the /activate_employee
        /<string:employee>_name endpoint returns status code 400
        if the employee is already active.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_employee/'
                          f'{self.get_employee().id}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_activate_empl_not_found(self):
        """
        Test that a PUT request to the /activate_employee
        /<int:employee_id> endpoint returns status code
        404 if the employee is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_employee/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
