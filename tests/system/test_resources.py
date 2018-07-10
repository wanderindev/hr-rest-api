import json

from tests.base_test import BaseTest


class TestResources(BaseTest):
    """System tests for the application resources."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a dict
        representing an organization and deleting users and
        organizations created in BaseTest.
        """
        super(TestResources, self).setUp()

    def test_post_with_authentication(self):
        """
        Test that POST requests to a resource's endpoint return
        status code 201 and the correct record.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    parsed_model = model.parse_model()
                    o_post, o_put = self.get_b_object(b_obj)

                    if o_post is not None:
                        with self.subTest(resource, o_post=o_post, user=user):
                            self.assertIsNone(
                                model.query.filter_by(**o_post).first())

                            result = c.post(f'/{endpoint}',
                                            data=json.dumps(o_post),
                                            headers=self.get_headers(user))

                            record = json.loads(result.data)['record']

                            self.assertEqual(201, result.status_code)

                            self.assertIsNotNone(model.query.filter_by(
                                id=record['id']).first())

                            self.check_record(o_post, record, parsed_model)

                            self.clear_db()

    def test_post_without_authentication(self):
        """
        Test that POST requests to a resource's endpoint return
        status code 401 if the user is not authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user('fake')
                    o_post, o_put = self.get_b_object(b_obj)

                    if o_post is not None:
                        with self.subTest(resource, o_post=o_post, user=user):
                            result = c.post(f'/{endpoint}',
                                            data=json.dumps(o_post),
                                            headers=self.get_headers(user))

                            self.assertEqual(401, result.status_code)

                            self.clear_db()

    def test_post_not_unique(self):
        """
        Test that POST requests to a resource's endpoint return
        status code 400 when violating a UNIQUE constraint.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    parsed_model = model.parse_model()
                    o_post, o_put = self.get_b_object(b_obj)

                    if parsed_model['unique']:
                        with self.subTest(resource, o_post=o_post, user=user):
                            self.assertIsNone(
                                model.query.filter_by(**o_post).first())

                            # POST object to db.
                            result = c.post(f'/{endpoint}',
                                            data=json.dumps(o_post),
                                            headers=self.get_headers(user))

                            self.assertEqual(201, result.status_code)

                            result = c.post(f'/{endpoint}',
                                            data=json.dumps(o_post),
                                            headers=self.get_headers(user))

                            self.assertEqual(400, result.status_code)

                            self.clear_db()

    def test_get_with_authentication(self):
        """
        Test that GET requests to a resource's endpoint return
        the correct record if the user is authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    parsed_model = model.parse_model()
                    o_post, o_put = self.get_b_object(b_obj)

                    if o_post is not None:
                        with self.subTest(resource, o_post=o_post, user=user):
                            # POST the object to the database and get the id.
                            result = c.post(f'/{endpoint}',
                                            data=json.dumps(o_post),
                                            headers=self.get_headers(user))
                            _id = json.loads(result.data)['record']['id']

                            # Make GET request.
                            result = c.get(f'/{endpoint}/{_id}',
                                           headers=self.get_headers(user))

                            record = json.loads(result.data)['record']

                            self.assertEqual(200, result.status_code)

                            self.check_record(o_post, record, parsed_model)

                            self.clear_db()

    def test_get_without_authentication(self):
        """
        Test that GET requests to a resource's endpoint return
        status code 401 if the user is not authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user('fake')
                    o_post, o_put = self.get_b_object(b_obj)

                    if o_post is not None:
                        with self.subTest(resource, user=user):
                            result = c.get(f'/{endpoint}/999',
                                           headers=self.get_headers(user))

                            self.assertEqual(401, result.status_code)

                            self.clear_db()

    def test_get_not_found(self):
        """
        Test that GET requests to a resource's endpoint return status
        code 404 if the record is not in the database.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    o_post, o_put = self.get_b_object(b_obj)

                    if o_post is not None:
                        with self.subTest(resource, user=user):
                            result = c.get(f'/{endpoint}/999',
                                           headers=self.get_headers(user))

                            self.assertEqual(404, result.status_code)

                            self.clear_db()

    def test_put_with_authentication(self):
        """
        Test that PUT requests to a resource's endpoint return
        status code 200 and the correct record.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    parsed_model = model.parse_model()
                    o_post, o_put = self.get_b_object(b_obj)

                    if o_post is not None:
                        with self.subTest(resource, o_put=o_put, user=user):
                            # POST the object to the database and get the id.
                            result = c.post(f'/{endpoint}',
                                            data=json.dumps(o_post),
                                            headers=self.get_headers(user))
                            _id = json.loads(result.data)['record']['id']

                            result = c.put(f'/{endpoint}/{_id}',
                                           data=json.dumps(o_put),
                                           headers=self.get_headers(user))

                            record = json.loads(result.data)['record']

                            self.assertEqual(200, result.status_code)

                            self.check_record(o_put, record, parsed_model)

                            self.clear_db()

    def test_put_without_authentication(self):
        """
        Test that PUT requests to a resource's endpoint return
        status code 401 if the user is not authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user('fake')
                    o_post, o_put = self.get_b_object(b_obj)

                    if o_post is not None:
                        with self.subTest(resource, o_put=o_put, user=user):
                            result = c.put(f'/{endpoint}/999',
                                           data=json.dumps(o_put),
                                           headers=self.get_headers(user))

                            self.assertEqual(401, result.status_code)

                            self.clear_db()

    def test_put_not_unique(self):
        """
        Test that PUT requests to a resource's endpoint return
        status code 400 when violating a UNIQUE constraint.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    parsed_model = model.parse_model()
                    o_post, o_put = self.get_b_object(b_obj)

                    if parsed_model['unique']:
                        with self.subTest(resource, o_put=o_put, user=user):
                            # POST the object to the database and get the id.
                            result = c.post(f'/{endpoint}',
                                            data=json.dumps(o_post),
                                            headers=self.get_headers(user))
                            _id = json.loads(result.data)['record']['id']

                            # POST a new object to the database.
                            c.post(f'/{endpoint}',
                                   data=json.dumps(o_put),
                                   headers=self.get_headers(user))

                            # PUT into original object data that violates
                            # unique contraint.
                            result = c.put(f'/{endpoint}/{_id}',
                                           data=json.dumps(o_put),
                                           headers=self.get_headers(user))

                            self.assertEqual(400, result.status_code)

                            self.clear_db()

    def test_put_not_found(self):
        """
        Test that PUT requests to a resource's endpoint return status
        code 404 if the record is not in the database.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    o_post, o_put = self.get_b_object(b_obj)

                    if o_post is not None:
                        with self.subTest(resource, o_put=o_put, user=user):
                            result = c.put(f'/{endpoint}/999',
                                           data=json.dumps(o_put),
                                           headers=self.get_headers(user))

                            self.assertEqual(404, result.status_code)

                            self.clear_db()

    def test_delete_with_authentication(self):
        """
        Test that a DELETE requests to a resource's endpoint return
        status code 200 if the user is authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    o_post, o_put = self.get_b_object(b_obj)

                    if o_post is not None:
                        with self.subTest(resource, o_post=o_post, user=user):
                            # POST the object to the database and get the id.
                            result = c.post(f'/{endpoint}',
                                            data=json.dumps(o_post),
                                            headers=self.get_headers(user))
                            _id = json.loads(result.data)['record']['id']

                            result = c.delete(f'/{endpoint}/{_id}',
                                              headers=self.get_headers(user))

                            self.assertEqual(200, result.status_code)

                            self.clear_db()

    def test_delete_without_authentication(self):
        """
        Test that a DELETE requests to a resource's endpoint return
        status code 401 if the user is not authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user('fake')
                    o_post, o_put = self.get_b_object(b_obj)

                    if o_post is not None:
                        with self.subTest(resource, user=user):
                            result = c.delete(f'/{endpoint}/999',
                                              headers=self.get_headers(user))

                            self.assertEqual(401, result.status_code)

                            self.clear_db()

    def test_delete_not_found(self):
        """
        Test that a DELETE requests to a resource's endpoint return
        status code 404 if the record is not in the database.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    o_post, o_put = self.get_b_object(b_obj)

                    if o_post is not None:
                        with self.subTest(resource, user=user):
                            result = c.delete(f'/{endpoint}/999',
                                              headers=self.get_headers(user))

                            self.assertEqual(404, result.status_code)

                            self.clear_db()

    def test_activate_inactivate_with_authentication(self):
        """
        Test that PUT requests to the resource's endpoint with is_active=False
        and is_active=True toggle the is_active state for the record.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    parsed_model = model.parse_model()
                    o_post, o_put = self.get_b_object(b_obj)

                    if 'is_active' in parsed_model['keys']:
                        with self.subTest(resource, o_post=o_post, user=user):
                            # POST the object to the database and get the id.
                            result = c.post(f'/{endpoint}',
                                            data=json.dumps(o_post),
                                            headers=self.get_headers(user))
                            _id = json.loads(result.data)['record']['id']

                            # Make record inactive
                            result = c.put(f'/activate_{endpoint}/{_id}',
                                           data=json.dumps({
                                               'is_active': False
                                           }),
                                           headers=self.get_headers(user))

                            self.assertEqual(200, result.status_code)

                            self.assertEqual('El registro fue inactivado.',
                                             json.loads(result.data)['message'])

                            # Make record active.
                            result = c.put(f'/activate_{endpoint}/{_id}',
                                           data=json.dumps({
                                               'is_active': True
                                           }),
                                           headers=self.get_headers(user))

                            self.assertEqual(200, result.status_code)

                            self.assertEqual('El registro fue activado.',
                                             json.loads(result.data)['message'])

                            self.clear_db()

    def test_activate_inactivate_active_inactive(self):
        """
        Test that PUT requests to the resource's endpoint with is_active=True
        and is_active=False return status code 400 if the record is already
        active or inactive.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    parsed_model = model.parse_model()
                    o_post, o_put = self.get_b_object(b_obj)

                    if 'is_active' in parsed_model['keys']:
                        with self.subTest(resource, o_post=o_post, user=user):
                            # POST the object to the database and get the id.
                            result = c.post(f'/{endpoint}',
                                            data=json.dumps(o_post),
                                            headers=self.get_headers(user))
                            _id = json.loads(result.data)['record']['id']

                            # Try to activate an active record.
                            result = c.put(f'/activate_{endpoint}/{_id}',
                                           data=json.dumps({
                                               'is_active': True
                                           }),
                                           headers=self.get_headers(user))

                            self.assertEqual(400, result.status_code)

                            self.assertEqual('El registro ya estaba activo.',
                                             json.loads(result.data)['message'])

                            # Make record inactive.
                            c.put(f'/activate_{endpoint}/{_id}',
                                  data=json.dumps({
                                      'is_active': False
                                  }),
                                  headers=self.get_headers(user))

                            # Try to inactivate an inactive record.
                            result = c.put(f'/activate_{endpoint}/{_id}',
                                           data=json.dumps({
                                               'is_active': False
                                           }),
                                           headers=self.get_headers(user))

                            self.assertEqual(400, result.status_code)

                            self.assertEqual('El registro ya estaba inactivo.',
                                             json.loads(result.data)['message'])

                            self.clear_db()

    def test_activate_without_authentication(self):
        """
        Test that a PUT requests to the resource's endpoint return
        status code 401 if user is not authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user('fake')
                    parsed_model = model.parse_model()

                    if 'is_active' in parsed_model['keys']:
                        with self.subTest(resource, user=user):
                            result = c.put(f'/activate_{endpoint}/999',
                                           data=json.dumps({
                                               'is_active': True
                                           }),
                                           headers=self.get_headers(user))

                            self.assertEqual(401, result.status_code)

                            self.clear_db()

    def test_activate_not_found(self):
        """
        Test that a PUT requests to the resource's endpoint return
        status code 404 if the record is not in the database.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    parsed_model = model.parse_model()

                    if 'is_active' in parsed_model['keys']:
                        with self.subTest(resource, user=user):
                            result = c.put(f'/activate_{endpoint}/999',
                                           data=json.dumps({
                                               'is_active': True
                                           }),
                                           headers=self.get_headers(user))

                            self.assertEqual(404, result.status_code)

                            self.clear_db()

    def test_list_with_authentication(self):
        """
        Test that GET requests to the resource's endpoint return the list
        of records if the user is authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user(user_type)
                    parsed_model = model.parse_model()
                    o_post, o_put = self.get_b_object(b_obj)

                    with self.subTest(resource, o_post=o_post, user=user):
                        if endpoint == 'marital_statuses':
                            result = c.get(f'/{endpoint}',
                                           headers=self.get_headers(user))
                        else:
                            # POST the object to the database and get the id.
                            result = c.post(f'/{endpoint}',
                                            data=json.dumps(o_post),
                                            headers=self.get_headers(user))
                            _id = json.loads(result.data)['record']['id']

                            if 'employee_id' in parsed_model['keys']:
                                result = c.get(f'/{endpoint}s'
                                               f'/{o_post["employee_id"]}',
                                               headers=self.get_headers(user))
                            else:
                                result = c.get(f'/{endpoint}s',
                                               headers=self.get_headers(user))

                        _list = json.loads(result.data)['list']

                        self.assertEqual(200, result.status_code)

                        self.assertGreater(len(_list), 0)

                        self.clear_db()

    def test_list_without_authentication(self):
        """
        Test that GET requests to the resource's endpoint return status
        code 401 if the user is not authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for params in self.get_system_test_params():
                    resource, model, b_obj, endpoint, user_type = params
                    user = self.get_test_user('fake')
                    parsed_model = model.parse_model()
                    o_post, o_put = self.get_b_object(b_obj)

                    with self.subTest(resource, user=user):
                        if endpoint == 'marital_statuses':
                            result = c.get(f'/{endpoint}',
                                           headers=self.get_headers(user))
                        else:
                            if 'employee_id' in parsed_model['keys']:
                                result = c.get(f'/{endpoint}s'
                                               f'/{o_post["employee_id"]}',
                                               headers=self.get_headers(user))
                            else:
                                result = c.get(f'/{endpoint}s',
                                               headers=self.get_headers(user))

                        self.assertEqual(401, result.status_code)

                        self.clear_db()
