import json

from models.marital_status import MaritalStatusModel
from tests.base_test import BaseTest


class TestMaritalStatus(BaseTest):
    """System tests for the marital_status resource."""
    def test_marital_status_list_with_authentication(self):
        """
        Test that GET requests to the /marital_statuses endpoint
        returns the list of marital_statuses if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get('/marital_statuses',
                          headers=self.get_headers())

                expected = {
                    'marital_statuses': list(map(lambda x: x.to_dict(),
                                                 MaritalStatusModel.find_all()))
                }

                expected_list = expected['marital_statuses']
                returned_list = json.loads(r.data)['marital_statuses']

                self.assertEqual(r.status_code, 200)
                self.assertListEqual(expected_list, returned_list)

    def test_marital_status_list_without_authentication(self):
        """
        Test that GET requests to the /marital_statuses endpoint
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint
                # with wrong authorization header.
                r = c.get('/marital_statuses',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)
