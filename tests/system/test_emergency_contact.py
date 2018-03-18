import json

from models.emergency_contact import EmergencyContactModel
from tests.base_test import BaseTest


class TestEmergencyContact(BaseTest):
    """System tests for the emergency contact resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a dict representing
        an emergency contact.
        """
        super(TestEmergencyContact, self).setUp()

        with self.app_context():
            self.e_c_dict = {
                'first_name': 'f_n',
                'last_name': 'l_n',
                'home_phone': '111-1111',
                'work_phone': '222-2222',
                'mobile_phone': '6666-6666',
                'employee_id': self.get_employee().id
            }

    def test_e_cont_post_with_authentication(self):
        """
        Test that a POST request to the /emergency_contact endpoint returns
        status code 201 and that the emergency contact is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/emergency_contact',
                           data=json.dumps(self.e_c_dict),
                           headers=self.get_headers())

                e_cont = json.loads(r.data)['emergency_contact']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(e_cont['first_name'],
                                 self.e_c_dict['first_name'])
                self.assertEqual(e_cont['last_name'],
                                 self.e_c_dict['last_name'])
                self.assertEqual(e_cont['home_phone'],
                                 self.e_c_dict['home_phone'])
                self.assertEqual(e_cont['work_phone'],
                                 self.e_c_dict['work_phone'])
                self.assertEqual(e_cont['mobile_phone'],
                                 self.e_c_dict['mobile_phone'])
                self.assertEqual(e_cont['employee_id'],
                                 self.e_c_dict['employee_id'])
                self.assertIsNotNone(EmergencyContactModel.find_by_id(
                    e_cont['id'], self.u))

    def test_e_cont_post_without_authentication(self):
        """
        Test that a POST request to the /emergency_contact endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /emergency_contact endpoint with
                # wrong authentication header.
                r = c.post('/emergency_contact',
                           data=json.dumps(self.e_c_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_e_cont_post_wrong_user(self):
        """
        Test that status code 403 is returned when trying to POST an
        emergency_contact with a user without permission.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/emergency_contact',
                           data=json.dumps(self.e_c_dict),
                           headers=self.get_headers({
                               'username': 'test_other_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 403)

    def test_e_cont_get_with_authentication(self):
        """
        Test that a GET request to the /emergency_contact/<id:contact_id>
        endpoint returns the correct emergency contact and status code 200 if
        the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/emergency_contact/'
                          f'{self.get_emergency_contact().id}',
                          headers=self.get_headers())

                e_cont = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(e_cont['first_name'],
                                 self.e_c_dict['first_name'])
                self.assertEqual(e_cont['last_name'],
                                 self.e_c_dict['last_name'])
                self.assertEqual(e_cont['home_phone'],
                                 self.e_c_dict['home_phone'])
                self.assertEqual(e_cont['work_phone'],
                                 self.e_c_dict['work_phone'])
                self.assertEqual(e_cont['mobile_phone'],
                                 self.e_c_dict['mobile_phone'])
                self.assertEqual(e_cont['employee_id'],
                                 self.e_c_dict['employee_id'])

    def test_e_cont_get_not_found(self):
        """
        Test that a GET request to the /emergency_contact/<id:contact_id>
        endpoint returns status code 404 if the emergency contact is not
        found in the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/emergency_contact/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_e_cont_get_without_authentication(self):
        """
        Test that a GET request to the /emergency_contact/<id:contact_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/emergency_contact/'
                          f'{self.get_emergency_contact().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_e_cont_put_with_authentication(self):
        """
        Test that a PUT request to the /emergency_contact/<id:contact_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/emergency_contact/'
                          f'{self.get_emergency_contact().id}',
                          data=json.dumps({
                              'first_name': 'new_f_n',
                              'last_name': 'new_l_n',
                              'home_phone': '333-3333',
                              'work_phone': '444-4444',
                              'mobile_phone': '6666-7777',
                              'employee_id': self.get_employee().id
                          }),
                          headers=self.get_headers())

                e_cont = json.loads(r.data)['emergency_contact']

                self.assertEqual(e_cont['first_name'],
                                 'new_f_n')
                self.assertEqual(e_cont['last_name'],
                                 'new_l_n')
                self.assertEqual(e_cont['home_phone'],
                                 '333-3333')
                self.assertEqual(e_cont['work_phone'],
                                 '444-4444')
                self.assertEqual(e_cont['mobile_phone'],
                                 '6666-7777')
                self.assertEqual(e_cont['employee_id'],
                                 self.get_employee().id)
                self.assertEqual(r.status_code, 200)

    def test_e_cont_put_without_authentication(self):
        """
        Test that a PUT request to the /emergency_contact/<id:contact_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/emergency_contact/'
                          f'{self.get_emergency_contact().id}',
                          data=json.dumps({
                              'first_name': 'new_f_n',
                              'last_name': 'new_l_n',
                              'home_phone': '333-3333',
                              'work_phone': '444-4444',
                              'mobile_phone': '6666-7777',
                              'employee_id': self.get_employee().id
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_e_cont_put_not_found(self):
        """
        Test that a PUT request to the /emergency_contact/<id:contact_id>
        endpoint returns status code 404 if the emergency contact is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/emergency_contact/1',
                          data=json.dumps({
                              'first_name': 'new_f_n',
                              'last_name': 'new_l_n',
                              'home_phone': '333-3333',
                              'work_phone': '444-4444',
                              'mobile_phone': '6666-7777',
                              'employee_id': self.get_employee().id
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_e_cont_delete_with_authentication(self):
        """
        Test that a DELETE request to the /emergency_contact/<id:contact_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/emergency_contact/'
                             f'{self.get_emergency_contact().id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_e_cont_delete_without_authentication(self):
        """
        Test that a DELETE request to the /emergency_contact/<id:contact_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/emergency_contact/'
                             f'{self.get_emergency_contact().id}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_e_cont_delete_not_found(self):
        """
        Test that a DELETE request to the /emergency_contact/<id:contact_id>
        endpoint returns status code 404 if the emergency contact is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/emergency_contact/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
