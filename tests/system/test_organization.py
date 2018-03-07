import json

from db import db
from models.organization import OrganizationModel
from models.user import AppUserModel
from tests.base_test import BaseTest


class TestOrganization(BaseTest):
    """System tests for the organization resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a dict
        representing an organization and deleting users and
        organizations created in BaseTest.
        """
        super(TestOrganization, self).setUp()
        with self.app_context():
            AppUserModel.query.filter(AppUserModel.id != 1).delete()
            OrganizationModel.query.filter(OrganizationModel.id != 1).delete()
            db.session.commit()

            self.o_dict = {
                'organization_name': 'test_o',
                'is_active': True
            }

    def test_organization_post_with_authentication(self):
        """
        Test that a POST request to the /organization endpoint returns
        status code 201 and that the organization is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                self.assertIsNone(OrganizationModel.query.filter_by(
                    organization_name=self.o_dict["organization_name"]).first())

                r = c.post('/organization',
                           data=json.dumps(self.o_dict),
                           headers=self.get_headers({
                               'username': 'jfeliu',
                               'password': '1234'
                           }))

                o = json.loads(r.data)['organization']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(o['organization_name'],
                                 self.o_dict['organization_name'])
                self.assertTrue(o['is_active'])
                self.assertIsNotNone(o['id'])
                self.assertListEqual(o['app_users'],
                                     [])
                self.assertListEqual(o['employment_positions'],
                                     [])
                self.assertListEqual(o['departments'],
                                     [])
                self.assertListEqual(o['shifts'],
                                     [])
                self.assertListEqual(o['uniform_items'],
                                     [])
                self.assertIsNotNone(OrganizationModel.query.filter_by(
                    id=o['id']).first())

    def test_organization_post_without_authentication(self):
        """
        Test that a POST request to the /organization
        endpoint returns status code 401 if the user is not
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /organization endpoint with
                # wrong authentication header.
                r = c.post('/organization',
                           data=json.dumps(self.o_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_organization_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicated data to the /organization endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/organization',
                       data=json.dumps(self.o_dict),
                       headers=self.get_headers({
                           'username': 'jfeliu',
                           'password': '1234'
                       }))

                # Send duplicated POST request.
                r = c.post('/organization',
                           data=json.dumps(self.o_dict),
                           headers=self.get_headers({
                               'username': 'jfeliu',
                               'password': '1234'
                           }))

                self.assertEqual(r.status_code, 400)

    def test_organization_post_not_super(self):
        """
        Test that status code 403 is returned when trying to
        POST data to the /organization endpoint with a user which
        is not a super-user.
        """
        with self.app() as c:
            with self.app_context():
                self.toggle_is_super()

                r = c.post('/organization',
                           data=json.dumps(self.o_dict),
                           headers=self.get_headers({
                               'username': 'jfeliu',
                               'password': '1234'
                           }))

                self.assertEqual(r.status_code, 403)

                self.toggle_is_super()

    def test_organization_get_with_authentication(self):
        """
        Test that a GET request to the /organization/<int:organization_id>
        endpoint returns the correct organization if the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/organization/{self.get_organization().id}',
                          headers=self.get_headers({
                              'username': 'jfeliu',
                              'password': '1234'
                          }))

                o = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(o['organization_name'],
                                 self.o_dict['organization_name'])

    def test_organization_get_not_found(self):
        """
        Test that a GET request to the /organization/<int:organization_id>
        endpoint returns status code 404 if the organization is not found
        in the database table or if the user does not belong to the
        organization and is not a super-user.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/organization/2',
                          headers=self.get_headers({
                              'username': 'jfeliu',
                              'password': '1234'
                          }))

                # Organization is not in the database.
                self.assertEqual(r.status_code, 404)

                organization_id = self.get_organization().id

                self.toggle_is_super()

                r = c.get(f'/organization/{organization_id}',
                          headers=self.get_headers({
                              'username': 'jfeliu',
                              'password': '1234'
                          }))

                # Organization is in the database but the user belongs to
                # another organization and it is not a super-user.
                self.assertEqual(r.status_code, 404)

                self.toggle_is_super()

    def test_organization_get_without_authentication(self):
        """
        Test that a GET request to the /organization/<int:organization_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the /organization endpoint with
                # wrong authentication header.
                r = c.get(f'/organization/1',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_organization_put_with_authentication(self):
        """
        Test that a PUT request to the /organization/<int:organization_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/organization/{self.get_organization().id}',
                          data=json.dumps({
                              'organization_name': 'new_test_o'
                          }),
                          headers=self.get_headers({
                              'username': 'jfeliu',
                              'password': '1234'
                          }))

                o = json.loads(r.data)['organization']

                self.assertEqual(r.status_code, 200)
                self.assertEqual(o['organization_name'],
                                 'new_test_o')
                self.assertTrue(o['is_active'])
                self.assertIsNotNone(o['id'])

    def test_organization_put_without_authentication(self):
        """
        Test that a PUT request to the /organization/<int:organization_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the /organization/<int:organization_id>
                # endpoint with wrong authorization header.
                r = c.put(f'/organization/1',
                          data=json.dumps({
                              'organization_name': 'new_test_o'
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_organization_put_not_found(self):
        """
        Test that a PUT request to the /organization/<int:organization_id>
        endpoint returns status code 404 if the organization is not in the
        database or if the user does not belong to the organization and
        is not a super-user.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/organization/2',
                          data=json.dumps({
                              'organization_name': 'new_test_o'
                          }),
                          headers=self.get_headers({
                              'username': 'jfeliu',
                              'password': '1234'
                          }))

                # Organization is not in the database.
                self.assertEqual(r.status_code, 404)

                organization_id = self.get_organization().id

                self.toggle_is_super()

                r = c.put(f'/organization/{organization_id}',
                          data=json.dumps({
                              'organization_name': 'new_test_o'
                          }),
                          headers=self.get_headers({
                              'username': 'jfeliu',
                              'password': '1234'
                          }))

                # Organization is in the database but the user belongs to
                # another organization and it is not a super-user.
                self.assertEqual(r.status_code, 404)

                self.toggle_is_super()

    def test_organization_delete_with_authentication(self):
        """
        Test that a DELETE request to the /organization/<int:organization_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/organization/{self.get_organization().id}',
                             headers=self.get_headers({
                                 'username': 'jfeliu',
                                 'password': '1234'
                             }))

                self.assertEqual(r.status_code, 200)

    def test_organization_delete_without_authentication(self):
        """
        Test that a DELETE request to the /organization/<int:organization_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the /organization/<int:organization_id>
                # endpoint with wrong authorization header.
                r = c.delete(f'/organization/1',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_organization_delete_inactive(self):
        """
        Test that a DELETE request to the /organization/<int:organization_id>
        endpoint returns status code 400 if the organization is not active.
        """
        with self.app() as c:
            with self.app_context():
                organization_id = self.get_organization().id

                c.delete(f'/organization/{organization_id}',
                         headers=self.get_headers({
                             'username': 'jfeliu',
                             'password': '1234'
                         }))

                # Repeat DELETE request.
                r = c.delete(f'/organization/{organization_id}',
                             headers=self.get_headers({
                                 'username': 'jfeliu',
                                 'password': '1234'
                             }))

                self.assertEqual(r.status_code, 400)

    def test_organization_delete_not_found(self):
        """
        Test that a DELETE request to the /organization/<int:organization_id>
        endpoint returns status code 404 if the organization is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/organization/2',
                             headers=self.get_headers({
                                 'username': 'jfeliu',
                                 'password': '1234'
                             }))

                self.assertEqual(r.status_code, 404)

    def test_organization_delete_not_super(self):
        """
        Test that a DELETE request to the /organization/<int:organization_id>
        endpoint returns status code 403 if the user is not a super-user.
        """
        with self.app() as c:
            with self.app_context():
                self.toggle_is_super()

                r = c.delete(f'/organization/1',
                             headers=self.get_headers({
                                 'username': 'jfeliu',
                                 'password': '1234'
                             }))

                self.assertEqual(r.status_code, 403)

                self.toggle_is_super()

    def test_activate_organization_with_authentication(self):
        """
        Test that a PUT request to the /activate_organization
        /<int:organization_id> endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                organization_id = self.get_organization().id

                c.delete(f'/organization/{organization_id}',
                         headers=self.get_headers({
                             'username': 'jfeliu',
                             'password': '1234'
                         }))

                r = c.put(f'/activate_organization/{organization_id}',
                          headers=self.get_headers({
                              'username': 'jfeliu',
                              'password': '1234'
                          }))

                self.assertEqual(r.status_code, 200)

    def test_activate_organization_without_authentication(self):
        """
        Test that a PUT request to the /activate_organization
        /<int:organization_id> endpoint returns status code
        401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_organization with
                # wrong authorization header.
                r = c.put(f'/activate_organization/1',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_activate_organization_active(self):
        """
        Test that a PUT request to the /activate_organization
        /<int:organization_id> endpoint returns status code
        400 if the organization is already active.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_organization/'
                          f'{self.get_organization().id}',
                          headers=self.get_headers({
                              'username': 'jfeliu',
                              'password': '1234'
                          }))

                self.assertEqual(r.status_code, 400)

    def test_activate_organization_not_found(self):
        """
        Test that a PUT request to the /activate_organization
        /<int:organization_id> endpoint returns status code
        404 if the organization was not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_organization/2',
                          headers=self.get_headers({
                              'username': 'jfeliu',
                              'password': '1234'
                          }))

                self.assertEqual(r.status_code, 404)

    def test_activate_organization_not_super(self):
        """
        Test that a PUT request to the /activate_organization
        /<int:organization_id> endpoint returns status code
        403 if the user is not a super-user.
        """
        with self.app() as c:
            with self.app_context():
                organization_id = self.get_organization().id

                self.toggle_is_super()

                r = c.put(f'/activate_organization/{organization_id}',
                          headers=self.get_headers({
                              'username': 'jfeliu',
                              'password': '1234'
                          }))

                self.assertEqual(r.status_code, 403)

                self.toggle_is_super()

    def test_organization_list_with_authentication(self):
        """
        Test that GET requests to the /organizations endpoint
        returns the list of organizations if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get('/organizations',
                          headers=self.get_headers({
                              'username': 'jfeliu',
                              'password': '1234'
                          }))

                organizations = json.loads(r.data)['organizations']

                self.assertEqual(r.status_code, 200)
                self.assertIn(OrganizationModel.query.filter_by(
                    id=1).first().to_dict(), organizations)

    def test_organization_list_without_authentication(self):
        """
        Test that GET requests to the /organizations endpoint
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint
                # with wrong authorization header.
                r = c.get('/organizations',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_organization_list_not_super(self):
        """
        Test that GET requests to the /organizations endpoint
        returns status code 403 if the user is not a super-user.
        """
        with self.app() as c:
            with self.app_context():
                self.toggle_is_super()

                r = c.get('/organizations',
                          headers=self.get_headers({
                              'username': 'jfeliu',
                              'password': '1234'
                          }))

                self.assertEqual(r.status_code, 403)

                self.toggle_is_super()
