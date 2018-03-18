import json

from models.uniform_requirement import UniformRequirementModel
from tests.base_test import BaseTest


class TestUniformItem(BaseTest):
    """System tests for the uniform requirement resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up two uniform sizes
        and a dict representing a uniform requirement.
        """
        super(TestUniformItem, self).setUp()

        with self.app_context():
            # Create uniform item with two sizes.
            self.u_i_1 = self.get_uniform_item()
            self.u_s_1 = self.get_uniform_size()
            self.u_s_2 = self.get_uniform_size({
                'size_description': 'new_test_u_s',
                'uniform_item_id': self.u_i_1.id
            })

            # Create another uniform item with one size.
            self.u_i_2 = self.get_uniform_item({
                'item_name': 'new_test_u_i',
                'organization_id': self.get_organization().id
            })
            self.u_s_3 = self.get_uniform_size({
                'size_description': 'another_test_u_s',
                'uniform_item_id': self.u_i_2.id
            })

            # Create a uniform item in another organization
            # with one uniform size.
            self.u_i_3 = self.get_uniform_item({
                'item_name': 'another_test_u_i',
                'organization_id': 1
            })
            self.u_s_4 = self.get_uniform_size({
                'size_description': 'yet_another_test_u_s',
                'uniform_item_id': self.u_i_3.id
            })

            self.u_r_dict = {
                'employee_id': self.get_employee().id,
                'uniform_item_id': self.u_i_1.id,
                'uniform_size_id': self.u_s_1.id
            }

    def test_u_req_post_with_authentication(self):
        """
        Test that a POST request to the /uniform_requirement endpoint returns
        status code 201 and that the uniform requirement is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/uniform_requirement',
                           data=json.dumps(self.u_r_dict),
                           headers=self.get_headers())

                u_r = json.loads(r.data)['uniform_requirement']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(u_r['employee_id'],
                                 self.u_r_dict['employee_id'])
                self.assertEqual(u_r['uniform_item_id'],
                                 self.u_r_dict['uniform_item_id'])
                self.assertEqual(u_r['uniform_size_id'],
                                 self.u_r_dict['uniform_size_id'])
                self.assertIsNotNone(UniformRequirementModel.find_by_id(
                    u_r['id'], self.u))

    def test_u_req_post_without_authentication(self):
        """
        Test that a POST request to the /uniform_requirement endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /uniform_requirement endpoint with
                # wrong authentication header.
                r = c.post('/uniform_requirement',
                           data=json.dumps(self.u_r_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_u_req_post_wrong_uniform_employee(self):
        """
        Test that a POST request to the /uniform_requirement endpoint
        returns status code 403 if the user has no access to the employee.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post(f'/uniform_requirement',
                           data=json.dumps({
                               'employee_id': self.u_r_dict['employee_id'],
                               'uniform_item_id': self.u_i_1.id,
                               'uniform_size_id': self.u_s_1.id
                           }),
                           headers=self.get_headers({
                               'username': 'test_other_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 403)

    def test_u_req_post_wrong_uniform_item(self):
        """
        Test that a POST request to the /uniform_requirement endpoint
        returns status code 403 if the user has no access to the uniform item.
        """
        with self.app() as c:
            with self.app_context():
                # Remove super user rights.
                self.u.is_super = False
                self.u.save_to_db()

                r = c.post(f'/uniform_requirement',
                           data=json.dumps({
                               'employee_id': self.u_r_dict['employee_id'],
                               'uniform_item_id': self.u_i_3.id,
                               'uniform_size_id': self.u_s_4.id
                           }),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 403)

    def test_u_req_post_wrong_uniform_size(self):
        """
        Test that a POST request to the /uniform_requirement endpoint
        returns status code 400 if the uniform size does not belong
        to the uniform item.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post(f'/uniform_requirement',
                           data=json.dumps({
                               'employee_id': self.u_r_dict['employee_id'],
                               'uniform_item_id': self.u_r_dict[
                                   'uniform_item_id'],
                               'uniform_size_id': self.u_s_3.id
                           }),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_u_req_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicated data to the /uniform_requirement endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/uniform_requirement',
                       data=json.dumps(self.u_r_dict),
                       headers=self.get_headers())

                # Send duplicated POST request.
                r = c.post('/uniform_requirement',
                           data=json.dumps(self.u_r_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_u_req_get_with_authentication(self):
        """
        Test that a GET request to the /uniform_requirement/<int:requirement_id>
        endpoint returns the correct uniform requirement and status code 200
        if the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/uniform_requirement/'
                          f'{self.get_uniform_requirement().id}',
                          headers=self.get_headers())

                u_r = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(u_r['employee_id'],
                                 self.u_r_dict['employee_id'])
                self.assertEqual(u_r['uniform_item_id'],
                                 self.u_r_dict['uniform_item_id'])
                self.assertEqual(u_r['uniform_size_id'],
                                 self.u_r_dict['uniform_size_id'])

    def test_u_req_get_not_found(self):
        """
        Test that a GET request to the /uniform_requirement/<int:requirement_id>
        endpoint returns status code 404 if the uniform requirement is not
        found in the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/uniform_requirement/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_u_req_get_without_authentication(self):
        """
        Test that a GET request to the /uniform_requirement/<int:requirement_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/uniform_requirement/'
                          f'{self.get_uniform_requirement().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_u_req_put_with_authentication(self):
        """
        Test that a PUT request to the /uniform_requirement/<int:requirement_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/uniform_requirement/'
                          f'{self.get_uniform_requirement().id}',
                          data=json.dumps({
                              'employee_id': self.u_r_dict['employee_id'],
                              'uniform_item_id': self.u_r_dict[
                                  'uniform_item_id'],
                              'uniform_size_id': self.u_s_2.id
                          }),
                          headers=self.get_headers())

                u_r = json.loads(r.data)['uniform_requirement']

                self.assertEqual(u_r['employee_id'],
                                 self.u_r_dict['employee_id'])
                self.assertEqual(u_r['uniform_item_id'],
                                 self.u_r_dict['uniform_item_id'])
                self.assertEqual(u_r['uniform_size_id'],
                                 self.u_s_2.id)
                self.assertEqual(r.status_code, 200)

    def test_u_req_put_without_authentication(self):
        """
        Test that a PUT request to the /uniform_requirement/<int:requirement_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/uniform_requirement/'
                          f'{self.get_uniform_requirement().id}',
                          data=json.dumps({
                              'employee_id': self.u_r_dict['employee_id'],
                              'uniform_item_id': self.u_r_dict[
                                  'uniform_item_id'],
                              'uniform_size_id': self.u_s_2.id
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_u_req_put_wrong_uniform_size(self):
        """
        Test that a PUT request to the /uniform_requirement/<int:requirement_id>
        endpoint returns status code 400 if the uniform size does not belong
        to the uniform item.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/uniform_requirement/'
                          f'{self.get_uniform_requirement().id}',
                          data=json.dumps({
                              'employee_id': self.u_r_dict['employee_id'],
                              'uniform_item_id': self.u_r_dict[
                                  'uniform_item_id'],
                              'uniform_size_id': self.u_s_3.id
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_u_req_put_not_found(self):
        """
        Test that a PUT request to the /uniform_requirement/<int:requirement_id>
        endpoint returns status code 404 if the uniform requirement is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/uniform_requirement/1',
                          data=json.dumps({
                              'employee_id': self.u_r_dict['employee_id'],
                              'uniform_item_id': self.u_r_dict[
                                  'uniform_item_id'],
                              'uniform_size_id': self.u_s_2.id
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_u_req_delete_with_authentication(self):
        """
        Test that a DELETE request to the /uniform_requirement
        /<int:requirement_id> endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/uniform_requirement/'
                             f'{self.get_uniform_requirement().id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_u_req_delete_without_authentication(self):
        """
        Test that a DELETE request to the /uniform_requirement
        /<int:requirement_id> endpoint returns status code 401
        if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/uniform_requirement/'
                             f'{self.get_uniform_requirement().id}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_u_req_delete_not_found(self):
        """
        Test that a DELETE request to the /uniform_requirement
        /<int:requirement_id> endpoint returns status code 404
        if the uniform requirement is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/uniform_requirement/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
