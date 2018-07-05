import json
import unittest

from tests.base_test import BaseTest
from tests.business_objects import Organization


class TestResources(BaseTest):
    """System tests for the application resources."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a dict
        representing an organization and deleting users and
        organizations created in BaseTest.
        """
        super(TestResources, self).setUp()

    def test_post_requests(self):
        """Test all post request to the application resources"""
        pass

    def test_put_requests(self):
        """Test all put request to the application resources"""
        pass

    def test_get_requests(self):
        """Test all get request to the application resources"""
        pass

    def test_delete_requests(self):
        """Test all delete request to the application resources"""
        pass

    @staticmethod
    def print_test_marker(mark, test_name, res_name):
        print(f'\n'
              f'{mark} "{test_name}" for {res_name} resource.')

    def run_test(self, test_name, res_name, _kwargs):
        test = getattr(self, test_name, 'test_not_found')

        self.print_test_marker('STARTS', test_name, res_name)
        test(**_kwargs)
        self.print_test_marker('ENDS', test_name, res_name)

    def run_tests_for_records(self, res, user):
        res_name = res['name']
        tests = res['tests']['system']['record']
        model = res['model']
        endpoint = res['endpoints']['record']
        b_objs = res['objects']
        verbs = ['post', 'get', 'put', 'delete']

        self.parsed_model = model.parse_model()

        for verb in verbs:
            for test_name in tests[verb]:
                _kwargs = {
                    'model': model,
                    'endpoint': endpoint,
                    'b_obj': b_objs[verb],
                    'user': user
                }
                self.run_test(test_name, res_name, _kwargs)

    def run_tests_for_activate(self):
        pass

    def run_tests_for_list(self):
        pass

    def test_all_resources(self):
        """Test all system tests for the application resources"""
        resources_to_test = [
            Organization
        ]

        for res in resources_to_test:
            if res['name'] is not 'Organization':
                self.create_users()
                user = self.test_user
            else:
                self.set_test_users()
                user = self.root_user

            if res['endpoints']['record'] is not None:
                self.run_tests_for_records(res, user)

            if res['endpoints']['activate'] is not None:
                self.run_tests_for_activate()

            if res['endpoints']['list'] is not None:
                self.run_tests_for_list()

    def test_not_found(self):
        print('Did not find test: ')

    def test_post_with_authentication(self, model, b_obj, endpoint, user):
        """
        Test that POST requests to a resource's endpoint return
        status code 201 and the correct business object.
        """
        with self.app() as c:
            with self.app_context():
                self.assertIsNone(
                    model.query.filter_by(**b_obj).first())

                result = c.post(endpoint,
                                data=json.dumps(b_obj),
                                headers=self.get_headers(user))

                record = json.loads(result.data)['record']

                self.assertEqual(201, result.status_code)

                self.assertIsNotNone(model.query.filter_by(
                    id=record['id']).first())

                self.check_record(b_obj, record)

    def test_post_without_authentication(self, model, b_obj, endpoint, user):
        """
        Test that POST requests to a resource's endpoint return
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                result = c.post(endpoint,
                                data=json.dumps(b_obj),
                                headers=self.get_headers(self.fake_user))

                self.assertEqual(401, result.status_code)

    def test_post_not_unique(self, model, b_obj, endpoint, user):
        """
        Test that POST requests to a resource's endpoint return
        status code 400 when violating a UNIQUE constraint.
        """
        with self.app() as c:
            with self.app_context():
                # POST the object to the database.
                c.post(endpoint,
                       data=json.dumps(b_obj),
                       headers=self.get_headers(user))

                # Send duplicated POST request.
                result = c.post(endpoint,
                                data=json.dumps(b_obj),
                                headers=self.get_headers(user))

                self.assertEqual(400, result.status_code)
