import json


from models.employee import EmployeeModel
from tests.base_test import BaseTest


class TestEmployee(BaseTest):
    """System tests for the employee resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a department, an
        employment position, a shift, and a dict representing an employee.
        """
        super(TestEmployee, self).setUp()

        with self.app_context():
            self.d = self.get_department(1)
            self.e_p = self.get_employment_position(1)
            self.s = self.get_shift(1)

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
                'department_id': self.d.id,
                'position_id': self.e_p.id,
                'shift_id': self.s.id
            }

    def test_empl_post_with_authentication(self):
        """
        Test that a POST request to the /employee endpoint returns
        status code 201 and that the employee is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/employee',
                           data=json.dumps(self.e_dict),
                           headers=self.get_headers())

                r_empl = json.loads(r.data)['employee']

                self.assertEqual(r.status_code, 201)
                self.assertTrue(r_empl['is_active'])
                self.assertTrue(r_empl['is_panamanian'])
                self.assertEqual(r_empl['first_name'],
                                 self.e_dict['first_name'])
                self.assertEqual(r_empl['second_name'],
                                 self.e_dict['second_name'])
                self.assertEqual(r_empl['first_surname'],
                                 self.e_dict['first_surname'])
                self.assertEqual(r_empl['second_surname'],
                                 self.e_dict['second_surname'])
                self.assertEqual(r_empl['gender'],
                                 self.e_dict['gender'])
                self.assertEqual(r_empl['national_id_number'],
                                 self.e_dict['national_id_number'])
                self.assertEqual(r_empl['date_of_birth'],
                                 self.e_dict['date_of_birth'])
                self.assertEqual(r_empl['address'],
                                 self.e_dict['address'])
                self.assertEqual(r_empl['home_phone'],
                                 self.e_dict['home_phone'])
                self.assertEqual(r_empl['mobile_phone'],
                                 self.e_dict['mobile_phone'])
                self.assertEqual(r_empl['email'],
                                 self.e_dict['email'])
                self.assertEqual(r_empl['type_of_contract'],
                                 self.e_dict['type_of_contract'])
                self.assertEqual(r_empl['payment_method'],
                                 self.e_dict['payment_method'])
                self.assertEqual(float(r_empl['salary_per_payment_period']),
                                 self.e_dict['salary_per_payment_period'])
                self.assertEqual(float(r_empl['representation_expenses_per'
                                              '_payment_period']),
                                 self.e_dict['representation_expenses_per'
                                             '_payment_period'])
                self.assertEqual(r_empl['employment_date'],
                                 self.e_dict['employment_date'])
                self.assertEqual(r_empl['contract_expiration_date'],
                                 self.e_dict['contract_expiration_date'])
                self.assertEqual(r_empl['termination_date'],
                                 self.e_dict['termination_date'])
                self.assertEqual(r_empl['termination_reason'],
                                 self.e_dict['termination_reason'])
                self.assertEqual(r_empl['position_id'],
                                 self.e_dict['position_id'])
                self.assertEqual(r_empl['department_id'],
                                 self.e_dict['department_id'])
                self.assertEqual(r_empl['marital_status_id'],
                                 self.e_dict['marital_status_id'])
                self.assertEqual(r_empl['shift_id'],
                                 self.e_dict['shift_id'])
                self.assertIsNotNone(EmployeeModel.find_by_id(r_empl['id'],
                                                              1))

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

    def test_empl_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicated data to the /employee endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/employee',
                       data=json.dumps(self.e_dict),
                       headers=self.get_headers())

                # Send duplicated POST request.
                r = c.post('/employee',
                           data=json.dumps(self.e_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_empl_get_with_authentication(self):
        """
        Test that a GET request to the /employee/<int:employee_id>
        endpoint returns the correct employee and status code 200 if the
        user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/employee',
                           data=json.dumps(self.e_dict),
                           headers=self.get_headers())

                employee_id = json.loads(r.data)['employee']['id']

                r = c.get(f'/employee/{employee_id}',
                          headers=self.get_headers())

                r_dict = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(r_dict['id'],
                                 employee_id)

    def test_empl_get_not_found(self):
        """
        Test that a GET request to the /employee/<int:employee_id>
        endpoint returns status code 404 if the employee is not found in
        the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/employee/test_d',
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
                r = c.get(f'/employee/1',
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
                r = c.post(f'/employee',
                           data=json.dumps(self.e_dict),
                           headers=self.get_headers())

                employee_id = json.loads(r.data)['employee']['id']

                r = c.put(f'/employee/{employee_id}',
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
                              'department_id': self.d.id,
                              'position_id': self.e_p.id,
                              'shift_id': self.s.id
                            }),
                          headers=self.get_headers())

                r_empl = json.loads(r.data)['employee']

                self.assertTrue(r_empl['is_active'])
                self.assertFalse(r_empl['is_panamanian'])
                self.assertEqual(r_empl['first_name'],
                                 'new_f_n')
                self.assertEqual(r_empl['second_name'],
                                 'new_s_n')
                self.assertEqual(r_empl['first_surname'],
                                 'new_f_sn')
                self.assertEqual(r_empl['second_surname'],
                                 'new_s_sn')
                self.assertEqual(r_empl['gender'],
                                 'Mujer')
                self.assertEqual(r_empl['national_id_number'],
                                 'N-1-11-111')
                self.assertEqual(r_empl['date_of_birth'],
                                 '2001-01-31')
                self.assertEqual(r_empl['address'],
                                 'Chiriquí')
                self.assertEqual(r_empl['home_phone'],
                                 '333-3333')
                self.assertEqual(r_empl['mobile_phone'],
                                 '6666-7777')
                self.assertEqual(r_empl['email'],
                                 'new_f_n@new_f_sn.com')
                self.assertEqual(r_empl['type_of_contract'],
                                 'Indefinido')
                self.assertEqual(r_empl['payment_method'],
                                 'Cheque')
                self.assertEqual(float(r_empl['salary_per_payment_period']),
                                 208)
                self.assertEqual(float(r_empl['representation_expenses_per'
                                              '_payment_period']),
                                 100)
                self.assertEqual(r_empl['employment_date'],
                                 '2019-01-01')
                self.assertEqual(r_empl['contract_expiration_date'],
                                 '2019-01-31')
                self.assertEqual(r_empl['termination_date'],
                                 '2019-01-15')
                self.assertEqual(r_empl['termination_reason'],
                                 'Renuncia')
                self.assertEqual(r_empl['position_id'],
                                 self.e_p.id)
                self.assertEqual(r_empl['department_id'],
                                 self.d.id)
                self.assertEqual(r_empl['marital_status_id'],
                                 2)
                self.assertEqual(r_empl['shift_id'],
                                 self.s.id)
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
                              'department_id': self.d.id,
                              'position_id': self.e_p.id,
                              'shift_id': self.s.id
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
                              'department_id': self.d.id,
                              'position_id': self.e_p.id,
                              'shift_id': self.s.id
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
                r = c.post('/employee',
                           data=json.dumps(self.e_dict),
                           headers=self.get_headers())

                employee_id = json.loads(r.data)['employee']['id']

                r = c.delete(f'/employee/{employee_id}',
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
                r = c.delete(f'/employee/1',
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
                r = c.post('/employee',
                           data=json.dumps(self.e_dict),
                           headers=self.get_headers())

                employee_id = json.loads(r.data)['employee']['id']

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
                r = c.post('/employee',
                           data=json.dumps(self.e_dict),
                           headers=self.get_headers())

                employee_id = json.loads(r.data)['employee']['id']

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
                r = c.put(f'/activate_employee/1',
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
                r = c.post('/employee',
                           data=json.dumps(self.e_dict),
                           headers=self.get_headers())

                employee_id = json.loads(r.data)['employee']['id']

                r = c.put(f'/activate_employee/{employee_id}',
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
