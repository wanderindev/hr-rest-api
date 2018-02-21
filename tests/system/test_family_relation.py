import json

from models.family_relation import FamilyRelationModel
from tests.base_test import BaseTest


class TestFamilyRelation(BaseTest):
    """System tests for the FamilyRelation resource."""
    def test_family_relation_list_with_authentication(self):
        """
        Test that GET requests to the /family_relations endpoint
        returns the list of family_relations if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get('/family_relations',
                          headers=self.get_headers())
                print(r)
                expected = {
                    'family_relations': list(
                        map(lambda x: x.to_dict(),
                            FamilyRelationModel.find_all()))
                }

                expected_list = expected['family_relations']
                returned_list = json.loads(r.data)['family_relations']

                self.assertEqual(r.status_code, 200)
                self.assertListEqual(expected_list, returned_list)

    def test_family_relation_list_without_authentication(self):
        """
        Test that GET requests to the /family_relations endpoint
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the endpoint
                # with wrong authorization header.
                r = c.get('/family_relations',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)
