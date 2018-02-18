import json

from models.uniform_size import UniformSizeModel
from tests.base_test import BaseTest


class TestUniformItem(BaseTest):
    """System tests for the uniform size resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a uniform
        item and a dict representing a uniform size.
        """
        super(TestUniformItem, self).setUp()

        with self.app_context():
            self.u_i = self.get_uniform_item(1)

            self.u_s_dict = {
                'size_description': 'test_u_s',
                'uniform_item_id': self.u_i.id
            }

    def test_u_size_post_with_authentication(self):
        """
        Test that a POST request to the /uniform_size endpoint returns
        status code 201 and that the uniform size is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                self.assertIsNone(UniformSizeModel.find_by_description(
                    self.u_s_dict['size_description'],
                    self.u_s_dict['uniform_item_id'],
                    self.u_i.organization_id))

                r = c.post('/uniform_size',
                           data=json.dumps(self.u_s_dict),
                           headers=self.get_headers())

                r_u_s = json.loads(r.data)['uniform_size']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(r_u_s['size_description'],
                                 self.u_s_dict['size_description'])
                self.assertEqual(r_u_s['uniform_item_id'],
                                 self.u_s_dict['uniform_item_id'])
                self.assertIsNotNone(UniformSizeModel.find_by_description(
                    self.u_s_dict['size_description'],
                    self.u_s_dict['uniform_item_id'],
                    self.u_i.organization_id))

    def test_u_size_post_without_authentication(self):
        """
        Test that a POST request to the /uniform_size endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /uniform_size endpoint with
                # wrong authentication header.
                r = c.post('/uniform_size',
                           data=json.dumps(self.u_s_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_u_size_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicated data to the /uniform_size endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/uniform_size',
                       data=json.dumps(self.u_s_dict),
                       headers=self.get_headers())

                # Send duplicated POST request.
                r = c.post('/uniform_size',
                           data=json.dumps(self.u_s_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_u_size_get_with_authentication(self):
        """
        Test that a GET request to the /uniform_size/<int:size_id>
        endpoint returns the correct uniform size and status code 200 if the
        user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/uniform_size',
                           data=json.dumps(self.u_s_dict),
                           headers=self.get_headers())

                size_id = json.loads(r.data)['uniform_size']['id']

                r = c.get(f'/uniform_size/{size_id}',
                          headers=self.get_headers())

                r_dict = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(r_dict['size_description'],
                                 self.u_s_dict['size_description'])

    def test_u_size_get_not_found(self):
        """
        Test that a GET request to the /uniform_size/<int:size_id>
        endpoint returns status code 404 if the uniform size is not found in
        the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/uniform_size/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_u_size_get_without_authentication(self):
        """
        Test that a GET request to the /uniform_size/<int:size_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/uniform_size/1',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_u_size_put_with_authentication(self):
        """
        Test that a PUT request to the /uniform_size/<int:size_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/uniform_size',
                           data=json.dumps(self.u_s_dict),
                           headers=self.get_headers())

                size_id = json.loads(r.data)['uniform_size']['id']

                r = c.put(f'/uniform_size/{size_id}',
                          data=json.dumps({
                              'size_description': 'new_test_u_s',
                              'uniform_item_id': self.u_s_dict[
                                  'uniform_item_id'],
                          }),
                          headers=self.get_headers())

                r_u_s = json.loads(r.data)['uniform_size']

                self.assertEqual(r_u_s['size_description'],
                                 'new_test_u_s')
                self.assertEqual(r_u_s['uniform_item_id'],
                                 self.u_s_dict['uniform_item_id'])
                self.assertEqual(r.status_code, 200)

    def test_u_size_put_without_authentication(self):
        """
        Test that a PUT request to the /uniform_size/<int:size_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/uniform_size/1',
                          data=json.dumps({
                              'size_description': 'new_test_u_s',
                              'uniform_item_id': self.u_s_dict[
                                  'uniform_item_id'],
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_u_size_put_not_found(self):
        """
        Test that a PUT request to the /uniform_size/<int:size_id>
        endpoint returns status code 404 if the uniform size is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/uniform_size/1',
                          data=json.dumps({
                              'size_description': 'new_test_u_s',
                              'uniform_item_id': self.u_s_dict[
                                  'uniform_item_id'],
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_u_size_delete_with_authentication(self):
        """
        Test that a DELETE request to the /uniform_size/<int:size_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/uniform_size',
                           data=json.dumps(self.u_s_dict),
                           headers=self.get_headers())

                size_id = json.loads(r.data)['uniform_size']['id']

                r = c.delete(f'/uniform_size/{size_id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_u_size_delete_without_authentication(self):
        """
        Test that a DELETE request to the /uniform_size/<int:size_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/uniform_size/1',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_u_size_delete_not_found(self):
        """
        Test that a DELETE request to the /uniform_size/<int:size_id>
        endpoint returns status code 404 if the uniform size is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/uniform_size/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
