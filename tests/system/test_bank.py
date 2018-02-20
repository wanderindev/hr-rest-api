import json

from models.bank import BankModel
from tests.base_test import BaseTest


class TestBank(BaseTest):
    """System tests for the bank resource."""
    def test_bank_list_with_authentication(self):
        """
        Test that GET requests to the /banks endpoint
        returns the list of banks if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get('/banks',
                          headers=self.get_headers())

                expected = {
                    'banks': list(map(lambda x: x.to_dict(),
                                      BankModel.find_all()))
                }

                expected_list = expected['banks']
                returned_list = json.loads(r.data)['banks']

                self.assertEqual(r.status_code, 200)
                self.assertListEqual(expected_list, returned_list)

    def test_bank_list_without_authentication(self):
        """
        Test that GET requests to the /banks endpoint
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint
                # with wrong authorization header.
                r = c.get('/banks',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)
