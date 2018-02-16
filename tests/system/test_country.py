import json

from models.country import CountryModel
from tests.base_test import BaseTest


class TestCountry(BaseTest):
    """System tests for the country resource."""
    def test_country_list_with_authentication(self):
        """
        Test that GET requests to the /countries endpoint
        returns the list of countries if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get('/countries',
                          headers=self.get_headers())

                expected = {
                    'countries': list(map(lambda x: x.to_dict(),
                                          CountryModel.find_all()))
                }

                expected_list = expected['countries']
                returned_list = json.loads(r.data)['countries']

                self.assertEqual(r.status_code, 200)
                self.assertListEqual(expected_list, returned_list)

    def test_country_list_without_authentication(self):
        """
        Test that GET requests to the /countries endpoint
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint
                # with wrong authorization header.
                r = c.get('/countries',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)
