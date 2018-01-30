import json

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
                # Get the marital_statuses list from the endpoint.
                r = c.get('/marital_statuses',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

                expected = {
                    'marital_statuses': [
                        {'status_feminine': 'Soltera', 'id': 1,
                         'status_masculine': 'Soltero'},
                        {'status_feminine': 'Unida', 'id': 2,
                         'status_masculine': 'Unido'},
                        {'status_feminine': 'Casada', 'id': 3,
                         'status_masculine': 'Casado'},
                        {'status_feminine': 'Divorciada', 'id': 4,
                         'status_masculine': 'Divorciado'},
                        {'status_feminine': 'Viuda', 'id': 5,
                         'status_masculine': 'Viudo'}
                    ]
                }

                e_m_s = expected['marital_statuses']
                m_s = json.loads(r.data)['marital_statuses']

                self.assertEqual(m_s[0]['id'], e_m_s[0]['id'])
                self.assertEqual(m_s[0]['status_feminine'],
                                 e_m_s[0]['status_feminine'])
                self.assertEqual(m_s[0]['status_masculine'],
                                 e_m_s[0]['status_masculine'])

                self.assertEqual(m_s[1]['id'], e_m_s[1]['id'])
                self.assertEqual(m_s[1]['status_feminine'],
                                 e_m_s[1]['status_feminine'])
                self.assertEqual(m_s[1]['status_masculine'],
                                 e_m_s[1]['status_masculine'])

                self.assertEqual(m_s[2]['id'], e_m_s[2]['id'])
                self.assertEqual(m_s[2]['status_feminine'],
                                 e_m_s[2]['status_feminine'])
                self.assertEqual(m_s[2]['status_masculine'],
                                 e_m_s[2]['status_masculine'])

                self.assertEqual(m_s[3]['id'], e_m_s[3]['id'])
                self.assertEqual(m_s[3]['status_feminine'],
                                 e_m_s[3]['status_feminine'])
                self.assertEqual(m_s[3]['status_masculine'],
                                 e_m_s[3]['status_masculine'])

                self.assertEqual(m_s[4]['id'], e_m_s[4]['id'])
                self.assertEqual(m_s[4]['status_feminine'],
                                 e_m_s[4]['status_feminine'])
                self.assertEqual(m_s[4]['status_masculine'],
                                 e_m_s[4]['status_masculine'])

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
