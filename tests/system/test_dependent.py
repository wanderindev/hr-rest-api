import json

from models.dependent import DependentModel
from tests.base_test import BaseTest


class TestDependent(BaseTest):
    """System tests for the dependent resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a
        dict representing an dependent.
        """
        super(TestDependent, self).setUp()

        with self.app_context():
            self.depen_dict = {
                'first_name': 'f_n',
                'second_name': 's_n',
                'first_surname': 'f_sn',
                'second_surname': 's_sn',
                'gender': 'Mujer',
                'date_of_birth': '2018-01-01',
                'employee_id': self.get_employee().id,
                'family_relation_id': 1
            }

    def test_depen_post_with_authentication(self):
        """
        Test that a POST request to the /dependent endpoint returns
        status code 201 and that the dependent is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/dependent',
                           data=json.dumps(self.depen_dict),
                           headers=self.get_headers())

                depen = json.loads(r.data)['dependent']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(depen['first_name'],
                                 self.depen_dict['first_name'])
                self.assertEqual(depen['second_name'],
                                 self.depen_dict['second_name'])
                self.assertEqual(depen['first_surname'],
                                 self.depen_dict['first_surname'])
                self.assertEqual(depen['second_surname'],
                                 self.depen_dict['second_surname'])
                self.assertEqual(depen['gender'],
                                 self.depen_dict['gender'])
                self.assertEqual(depen['date_of_birth'],
                                 self.depen_dict['date_of_birth'])
                self.assertEqual(depen['employee_id'],
                                 self.depen_dict['employee_id'])
                self.assertEqual(depen['family_relation_id'],
                                 self.depen_dict['family_relation_id'])
                self.assertIsNotNone(DependentModel.find_by_id(depen['id'],
                                                               self.u))

    def test_depen_post_without_authentication(self):
        """
        Test that a POST request to the /dependent endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /dependent endpoint with
                # wrong authentication header.
                r = c.post('/dependent',
                           data=json.dumps(self.depen_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)
                
    def test_depen_post_wrong_user(self):
        """
        Test that status code 403 is returned when trying to POST an
        dependent with a user without permission.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/dependent',
                           data=json.dumps(self.depen_dict),
                           headers=self.get_headers({
                               'username': 'test_other_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 403)

    def test_depen_get_with_authentication(self):
        """
        Test that a GET request to the /dependent/<int:dependent_id>
        endpoint returns the correct dependent and status code 200 if
        the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/dependent/{self.get_dependent().id}',
                          headers=self.get_headers())

                depen = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(depen['first_name'],
                                 self.depen_dict['first_name'])
                self.assertEqual(depen['second_name'],
                                 self.depen_dict['second_name'])
                self.assertEqual(depen['first_surname'],
                                 self.depen_dict['first_surname'])
                self.assertEqual(depen['second_surname'],
                                 self.depen_dict['second_surname'])
                self.assertEqual(depen['gender'],
                                 self.depen_dict['gender'])
                self.assertEqual(depen['date_of_birth'],
                                 self.depen_dict['date_of_birth'])
                self.assertEqual(depen['employee_id'],
                                 self.depen_dict['employee_id'])
                self.assertEqual(depen['family_relation_id'],
                                 self.depen_dict['family_relation_id'])

    def test_depen_get_not_found(self):
        """
        Test that a GET request to the /dependent/<int:dependent_id>
        endpoint returns status code 404 if the dependent is not
        found in the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/dependent/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_depen_get_without_authentication(self):
        """
        Test that a GET request to the /dependent/<int:dependent_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/dependent/1',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_depen_put_with_authentication(self):
        """
        Test that a PUT request to the /dependent/<int:dependent_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/dependent/{self.get_dependent().id}',
                          data=json.dumps({
                              'first_name': 'new_f_n',
                              'second_name': 'new_s_n',
                              'first_surname': 'new_f_sn',
                              'second_surname': 'new_s_sn',
                              'gender': 'Hombre',
                              'date_of_birth': '2018-01-31',
                              'employee_id': self.get_employee().id,
                              'family_relation_id': 2
                          }),
                          headers=self.get_headers())

                depen = json.loads(r.data)['dependent']

                self.assertEqual(depen['first_name'], 'new_f_n')
                self.assertEqual(depen['second_name'], 'new_s_n')
                self.assertEqual(depen['first_surname'], 'new_f_sn')
                self.assertEqual(depen['second_surname'], 'new_s_sn')
                self.assertEqual(depen['gender'], 'Hombre')
                self.assertEqual(depen['date_of_birth'], '2018-01-31')
                self.assertEqual(depen['employee_id'],
                                 self.depen_dict['employee_id'])
                self.assertEqual(depen['family_relation_id'], 2)
                self.assertEqual(r.status_code, 200)

    def test_depen_put_without_authentication(self):
        """
        Test that a PUT request to the /dependent/<int:dependent_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/dependent/{self.get_dependent().id}',
                          data=json.dumps({
                              'first_name': 'new_f_n',
                              'second_name': 'new_s_n',
                              'first_surname': 'new_f_sn',
                              'second_surname': 'new_s_sn',
                              'gender': 'Hombre',
                              'date_of_birth': '2018-01-31',
                              'employee_id': self.get_employee().id,
                              'family_relation_id': 2
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_depen_put_not_found(self):
        """
        Test that a PUT request to the /dependent/<int:dependent_id>
        endpoint returns status code 404 if the dependent is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/dependent/1',
                          data=json.dumps({
                              'first_name': 'new_f_n',
                              'second_name': 'new_s_n',
                              'first_surname': 'new_f_sn',
                              'second_surname': 'new_s_sn',
                              'gender': 'Hombre',
                              'date_of_birth': '2018-01-31',
                              'employee_id': self.get_employee().id,
                              'family_relation_id': 2
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_depen_delete_with_authentication(self):
        """
        Test that a DELETE request to the /dependent/<int:dependent_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/dependent/{self.get_dependent().id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_depen_delete_without_authentication(self):
        """
        Test that a DELETE request to the /dependent/<int:dependent_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/dependent/{self.get_dependent().id}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_depen_delete_not_found(self):
        """
        Test that a DELETE request to the /dependent/<int:dependent_id>
        endpoint returns status code 404 if the dependent is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/dependent/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
