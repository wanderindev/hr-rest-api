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

            self.m_o_dict = {
                'organization_name': 'new_test_o',
                'is_active': False
            }

            self.parsed_model = OrganizationModel.parse_model()

    def test_organization_post_with_authentication(self):
        """
        Test that a POST request to the /organization endpoint returns
        status code 201 and that the organization is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                self.assertIsNone(
                    OrganizationModel.query.filter_by(**self.o_dict).first())

                result = c.post('/organization',
                                data=json.dumps(self.o_dict),
                                headers=self.get_headers({
                                    'username': 'jfeliu',
                                    'password': '1234'
                                }))

                record = json.loads(result.data)['record']

                self.assertEqual(201, result.status_code)

                self.assertIsNotNone(OrganizationModel.query.filter_by(
                    id=record['id']).first())

                self.check_record(self.o_dict, record)

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
                result = c.post('/organization',
                                data=json.dumps(self.o_dict),
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': 'JWT FaKeToKeN!!'
                                })

                self.assertEqual(401, result.status_code)

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
                result = c.post('/organization',
                                data=json.dumps(self.o_dict),
                                headers=self.get_headers({
                                    'username': 'jfeliu',
                                    'password': '1234'
                                }))

                self.assertEqual(400, result.status_code)

    def test_organization_post_not_super(self):
        """
        Test that status code 403 is returned when trying to
        POST data to the /organization endpoint with a user which
        is not a super-user.
        """
        pass

    def test_organization_get_with_authentication(self):
        """
        Test that a GET request to the /organization/<int:organization_id>
        endpoint returns the correct organization if the user is authenticated.
        """
        with self.app() as c:
            with self.app_context():
                result = c.get(f'/organization/{self.get_organization().id}',
                               headers=self.get_headers({
                                   'username': 'jfeliu',
                                   'password': '1234'
                               }))

                record = json.loads(result.data)['record']

                self.assertEqual(200, result.status_code)

                self.check_record(self.o_dict, record)

    def test_organization_get_not_found(self):
        """
        Test that a GET request to the /organization/<int:organization_id>
        endpoint returns status code 404 if the organization is not found
        in the database table or if the user does not belong to the
        organization and is not a super-user.
        """
        with self.app() as c:
            with self.app_context():
                result = c.get(f'/organization/2',
                               headers=self.get_headers({
                                   'username': 'jfeliu',
                                   'password': '1234'
                               }))

                # Organization is not in the database.
                self.assertEqual(404, result.status_code)

                organization_id = self.get_organization().id

                self.toggle_is_super()

                result = c.get(f'/organization/{organization_id}',
                               headers=self.get_headers({
                                   'username': 'jfeliu',
                                   'password': '1234'
                               }))

                # Organization is in the database but the user belongs to
                # another organization and it is not a super-user.
                self.assertEqual(404, result.status_code)

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
                result = c.get(f'/organization/1',
                               headers={
                                   'Content-Type': 'application/json',
                                   'Authorization': 'JWT FaKeToKeN!!'
                               })

                self.assertEqual(401, result.status_code)

    def test_organization_put_with_authentication(self):
        """
        Test that a PUT request to the /organization/<int:organization_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                result = c.put(f'/organization/{self.get_organization().id}',
                               data=json.dumps(self.m_o_dict),
                               headers=self.get_headers({
                                   'username': 'jfeliu',
                                   'password': '1234'
                               }))

                record = json.loads(result.data)['record']

                self.assertEqual(200, result.status_code)

                self.check_record(self.m_o_dict, record)

    def test_organization_put_without_authentication(self):
        """
        Test that a PUT request to the /organization/<int:organization_id>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the /organization/<int:organization_id>
                # endpoint with wrong authorization header.
                result = c.put(f'/organization/1',
                               data=json.dumps(self.m_o_dict),
                               headers={
                                   'Content-Type': 'application/json',
                                   'Authorization': 'JWT FaKeToKeN!!'
                               })

                self.assertEqual(401, result.status_code)

    def test_organization_put_not_found(self):
        """
        Test that a PUT request to the /organization/<int:organization_id>
        endpoint returns status code 404 if the organization is not in the
        database or if the user does not belong to the organization and
        is not a super-user.
        """
        with self.app() as c:
            with self.app_context():
                result = c.put(f'/organization/2',
                               data=json.dumps(self.m_o_dict),
                               headers=self.get_headers({
                                   'username': 'jfeliu',
                                   'password': '1234'
                               }))

                # Organization is not in the database.
                self.assertEqual(404, result.status_code)

                organization_id = self.get_organization().id

                self.toggle_is_super()

                result = c.put(f'/organization/{organization_id}',
                               data=json.dumps(self.m_o_dict),
                               headers=self.get_headers({
                                   'username': 'jfeliu',
                                   'password': '1234'
                               }))

                # Organization is in the database but the user belongs to
                # another organization and it is not a super-user.
                self.assertEqual(404, result.status_code)

                self.toggle_is_super()

    def test_organization_delete_with_authentication(self):
        """
        Test that a DELETE request to the /organization/<int:organization_id>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                result = c.delete(f'/organization/{self.get_organization().id}',
                                  headers=self.get_headers({
                                      'username': 'jfeliu',
                                      'password': '1234'
                                  }))

                self.assertEqual(200, result.status_code)

    def test_organization_delete_without_authentication(self):
        """
        Test that a DELETE request to the /organization/<int:organization_id>
        endpoint returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the /organization/<int:organization_id>
                # endpoint with wrong authorization header.
                result = c.delete(f'/organization/1',
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Authorization': 'JWT FaKeToKeN!!'
                                  })

                self.assertEqual(401, result.status_code)

    def test_organization_delete_not_found(self):
        """
        Test that a DELETE request to the /organization/<int:organization_id>
        endpoint returns status code 404 if the organization is not found.
        """
        with self.app() as c:
            with self.app_context():
                result = c.delete(f'/organization/2',
                                  headers=self.get_headers({
                                      'username': 'jfeliu',
                                      'password': '1234'
                                  }))

                self.assertEqual(404, result.status_code)

    def test_organization_delete_not_super(self):
        """
        Test that a DELETE request to the /organization/<int:organization_id>
        endpoint returns status code 403 if the user is not a super-user.
        """
        pass

    def test_activate_inactivate_organization_with_authentication(self):
        """
        Test that PUT requests to the /activate_organization
        /<int:organization_id> endpoint with is_active=False and
        is_active=True toggles the is_active state for the organization.
        """
        with self.app() as c:
            with self.app_context():
                organization_id = self.get_organization().id

                # Make organization inactive
                result = c.put(f'/activate_organization/{organization_id}',
                               data=json.dumps({'is_active': False}),
                               headers=self.get_headers({
                                   'username': 'jfeliu',
                                   'password': '1234'
                               }))

                self.assertEqual(200, result.status_code)

                self.assertEqual('El registro fue inactivado.',
                                 json.loads(result.data)['message'])

                # Make organization active.
                result = c.put(f'/activate_organization/{organization_id}',
                               data=json.dumps({'is_active': True}),
                               headers=self.get_headers({
                                   'username': 'jfeliu',
                                   'password': '1234'
                               }))
                print(result)
                self.assertEqual(200, result.status_code)

                self.assertEqual('El registro fue activado.',
                                 json.loads(result.data)['message'])

    def test_activate_inactivate_organization_active_inactive(self):
        """
        Test that PUT requests to the /activate_organization
        /<int:organization_id> endpoint with is_active=True and
        is_active=False returns status code 400 if the organization
        is already active or inactive.
        """
        with self.app() as c:
            with self.app_context():
                organization_id = self.get_organization().id

                # Activate an already active organization.
                result = c.put(f'/activate_organization/{organization_id}',
                               data=json.dumps({'is_active': True}),
                               headers=self.get_headers({
                                   'username': 'jfeliu',
                                   'password': '1234'
                               }))

                self.assertEqual(400, result.status_code)

                self.assertEqual('El registro ya estaba activo.',
                                 json.loads(result.data)['message'])

                # Make organization inactive
                c.put(f'/activate_organization/{organization_id}',
                      data=json.dumps({'is_active': False}),
                      headers=self.get_headers({
                          'username': 'jfeliu',
                          'password': '1234'
                      }))

                # Inactivate an already inactive organization.
                result = c.put(f'/activate_organization/{organization_id}',
                               data=json.dumps({'is_active': False}),
                               headers=self.get_headers({
                                   'username': 'jfeliu',
                                   'password': '1234'
                               }))

                self.assertEqual(400, result.status_code)

                self.assertEqual('El registro ya estaba inactivo.',
                                 json.loads(result.data)['message'])

    def test_activate_organization_without_authentication(self):
        """
        Test that a PUT request to the /activate_organization
        /<int:organization_id> endpoint returns status code
        401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                organization_id = self.get_organization().id

                result = c.put(f'/activate_organization/{organization_id}',
                               data=json.dumps({'is_active': False}),
                               headers={
                                   'Content-Type': 'application/json',
                                   'Authorization': 'JWT FaKeToKeN!!'
                               })

                self.assertEqual(401, result.status_code)

    def test_activate_organization_not_found(self):
        """
        Test that a PUT request to the /activate_organization
        /<int:organization_id> endpoint returns status code
        404 if the organization was not found.
        """
        with self.app() as c:
            with self.app_context():
                result = c.put(f'/activate_organization/2',
                               data=json.dumps({'is_active': False}),
                               headers=self.get_headers({
                                   'username': 'jfeliu',
                                   'password': '1234'
                               }))

                self.assertEqual(404, result.status_code)

    def test_activate_organization_not_super(self):
        """
        Test that a PUT request to the /activate_organization
        /<int:organization_id> endpoint returns status code
        403 if the user is not a super-user.
        """
        pass

    def test_organization_list_with_authentication(self):
        """
        Test that GET requests to the /organizations endpoint
        returns the list of organizations if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                result = c.get('/organizations',
                               headers=self.get_headers({
                                   'username': 'jfeliu',
                                   'password': '1234'
                               }))

                _list = json.loads(result.data)['list']

                self.assertEqual(200, result.status_code)

                self.assertIn(OrganizationModel.query.filter_by(id=1)
                              .first()
                              .to_dict(), _list)

    def test_organization_list_without_authentication(self):
        """
        Test that GET requests to the /organizations endpoint
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint
                # with wrong authorization header.
                result = c.get('/organizations',
                               headers={
                                   'Content-Type': 'application/json',
                                   'Authorization': 'JWT FaKeToKeN!!'
                               })

                self.assertEqual(401, result.status_code)

    def test_organization_list_not_super(self):
        """
        Test that GET requests to the /organizations endpoint
        returns status code 403 if the user is not a super-user.
        """
        pass
