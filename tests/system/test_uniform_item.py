import json

from models.uniform_item import UniformItemModel
from tests.base_test import BaseTest


class TestUniformItem(BaseTest):
    """System tests for the uniform item resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a dict representing
        a uniform item.
        """
        super(TestUniformItem, self).setUp()

        with self.app_context():
            self.u_i_dict = {
                'item_name': 'test_u_i',
                'organization_id': self.get_organization().id
            }

    def test_u_item_post_with_authentication(self):
        """
        Test that a POST request to the /uniform_item endpoint returns
        status code 201 and that the uniform item is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                self.assertIsNone(UniformItemModel.query.filter_by(
                    item_name=self.u_i_dict['item_name'],
                    organization_id=self.u_i_dict['organization_id']).first())

                r = c.post('/uniform_item',
                           data=json.dumps(self.u_i_dict),
                           headers=self.get_headers())

                u_i = json.loads(r.data)['uniform_item']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(u_i['item_name'],
                                 self.u_i_dict['item_name'])
                self.assertEqual(u_i['organization_id'],
                                 self.u_i_dict['organization_id'])
                self.assertIsNotNone(UniformItemModel.query.filter_by(
                    item_name=self.u_i_dict['item_name'],
                    organization_id=self.u_i_dict['organization_id']).first())

    def test_u_item_post_without_authentication(self):
        """
        Test that a POST request to the /uniform_item endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /uniform_item endpoint with
                # wrong authentication header.
                r = c.post('/uniform_item',
                           data=json.dumps(self.u_i_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_u_item_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicated data to the /uniform_item endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/uniform_item',
                       data=json.dumps(self.u_i_dict),
                       headers=self.get_headers())

                # Send duplicated POST request.
                r = c.post('/uniform_item',
                           data=json.dumps(self.u_i_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)
                
    def test_u_item_get_with_authentication(self):
        """
        Test that a GET request to the /uniform_item/<int:item_id>
        endpoint returns the correct uniform item and status code 200 if the
        user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/uniform_item/{self.get_uniform_item().id}',
                          headers=self.get_headers())

                u_i = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(u_i['item_name'],
                                 self.u_i_dict['item_name'])

    def test_u_item_get_not_found(self):
        """
        Test that a GET request to the /uniform_item/<int:item_id>
        endpoint returns status code 404 if the uniform item is not found in
        the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/uniform_item/1',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_u_item_get_without_authentication(self):
        """
        Test that a GET request to the /uniform_item/<int:item_id>
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint with
                # wrong authentication header.
                r = c.get(f'/uniform_item/{self.get_uniform_item().id}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_u_item_put_with_authentication(self):
        """
        Test that a PUT request to the /uniform_item/<int:item_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/uniform_item/{self.get_uniform_item().id}',
                          data=json.dumps({
                              'item_name': 'new_test_u_i',
                              'organization_id': self.get_organization().id
                          }),
                          headers=self.get_headers())

                u_i = json.loads(r.data)['uniform_item']

                self.assertEqual(u_i['item_name'],
                                 'new_test_u_i')
                self.assertEqual(u_i['organization_id'],
                                 self.u_i_dict['organization_id'])
                self.assertEqual(r.status_code, 200)

    def test_u_item_put_without_authentication(self):
        """
        Test that a PUT request to the /uniform_item/<int:item_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the endpoint with
                # wrong authentication header.
                r = c.put(f'/uniform_item/{self.get_uniform_item().id}',
                          data=json.dumps({
                              'item_name': 'new_test_u_i',
                              'organization_id':  self.get_organization().id
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_u_item_put_not_found(self):
        """
        Test that a PUT request to the /uniform_item/<int:item_id>
        endpoint returns status code 404 if the uniform item is not
        in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/uniform_item/1',
                          data=json.dumps({
                              'item_name': 'new_test_u_i',
                              'organization_id':  self.get_organization().id
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_u_item_delete_with_authentication(self):
        """
        Test that a DELETE request to the /uniform_item/<int:item_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/uniform_item/{self.get_uniform_item().id}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_u_item_delete_without_authentication(self):
        """
        Test that a DELETE request to the /uniform_item/<int:item_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the endpoint
                # with wrong authorization header.
                r = c.delete(f'/uniform_item/{self.get_uniform_item().id}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_u_item_delete_not_found(self):
        """
        Test that a DELETE request to the /uniform_item/<int:item_id>
        endpoint returns status code 404 if the uniform item is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/uniform_item/1',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
