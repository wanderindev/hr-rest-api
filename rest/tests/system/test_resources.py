import json
from copy import deepcopy

from flask import current_app

from tests.base_test import BaseTest
from tests.business_objects import get_sys_test_params, get_item_from_db, \
    OBJECTS_TO_TEST, RAW_ATTENDANCE


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
                for obj in OBJECTS_TO_TEST:
                    resource, model, post_items, _, endpoints, \
                        user = get_sys_test_params(obj, 0, 'first')

                    parsed_model = model.parse_model()

                    if endpoints[0]:
                        item = post_items[0]

                        with self.subTest(resource, item=item, user=user):
                            if 'password' in parsed_model['keys']:
                                o = dict(item)
                                o.pop('password')
                                self.assertIsNone(
                                    model.query.filter_by(**o).first())
                            else:
                                self.assertIsNone(
                                    model.query.filter_by(**item).first())

                            result = c.post(f'/{endpoints[0]}',
                                            data=json.dumps(item),
                                            headers=self.get_headers(user))

                            record = json.loads(result.data)['record']

                            self.check_record(item, record, parsed_model)

                            self.assertIsNotNone(model.query.filter_by(
                                id=record['id']).first())

                            self.assertEqual(201, result.status_code)

                            # Clear the db and cache at the end of the subtest.
                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_post_without_authentication(self):
        """
        Test that POST requests to a resource's endpoint return
        status code 401 if the user is not authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, post_items, _, endpoints, \
                        user = get_sys_test_params(obj, 0, 'first',
                                                   'none', 'fake')

                    if endpoints[0]:
                        item = post_items[0]

                        with self.subTest(resource, item=item, user=user):
                            result = c.post(f'/{endpoints[0]}',
                                            data=json.dumps(item),
                                            headers=self.get_headers(user))

                            self.assertEqual(401, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_post_not_unique(self):
        """
        Test that POST requests to a resource's endpoint return
        status code 400 when violating a UNIQUE constraint.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, post_items, _, endpoints, \
                        user = get_sys_test_params(obj, 0, 'first')

                    parsed_model = model.parse_model()

                    if endpoints[0] and parsed_model['unique']:
                        item = post_items[0]

                        with self.subTest(resource, item=item, user=user):
                            if 'password' in parsed_model['keys']:
                                o = dict(item)
                                o.pop('password')
                                self.assertIsNone(
                                    model.query.filter_by(**o).first())
                            else:
                                self.assertIsNone(
                                    model.query.filter_by(**item).first())

                            result = c.post(f'/{endpoints[0]}',
                                            data=json.dumps(item),
                                            headers=self.get_headers(user))

                            self.assertEqual(201, result.status_code)

                            result = c.post(f'/{endpoints[0]}',
                                            data=json.dumps(item),
                                            headers=self.get_headers(user))

                            self.assertEqual(400, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_get_with_authentication(self):
        """
        Test that GET requests to a resource's endpoint return
        the correct record if the user is authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, post_items, _, endpoints, \
                        user = get_sys_test_params(obj, 0, 'first')

                    parsed_model = model.parse_model()

                    if endpoints[0]:
                        item = post_items[0]

                        with self.subTest(resource, item=item, user=user):
                            # POST the object to the database and get the id.
                            result = c.post(f'/{endpoints[0]}',
                                            data=json.dumps(item),
                                            headers=self.get_headers(user))
                            _id = json.loads(result.data)['record']['id']

                            # Make GET request.
                            result = c.get(f'/{endpoints[0]}/{_id}',
                                           headers=self.get_headers(user))

                            record = json.loads(result.data)['record']

                            self.assertEqual(200, result.status_code)

                            self.check_record(item, record, parsed_model)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_get_without_authentication(self):
        """
        Test that GET requests to a resource's endpoint return
        status code 401 if the user is not authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, _, _, endpoints, \
                        user = get_sys_test_params(obj, 0, 'none',
                                                   'none', 'fake')

                    if endpoints[0]:
                        with self.subTest(resource, user=user):
                            result = c.get(f'/{endpoints[0]}/999',
                                           headers=self.get_headers(user))

                            self.assertEqual(401, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_get_not_found(self):
        """
        Test that GET requests to a resource's endpoint return status
        code 404 if the record is not in the database.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, _, _, endpoints, \
                        user = get_sys_test_params(obj, 0)

                    if endpoints[0]:
                        with self.subTest(resource, user=user):
                            result = c.get(f'/{endpoints[0]}/999',
                                           headers=self.get_headers(user))

                            self.assertEqual(404, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_put_with_authentication(self):
        """
        Test that PUT requests to a resource's endpoint return
        status code 200 and the correct record.
        """
        with self.client() as c:
            with self.app_context():
                with self.app_context():
                    for obj in OBJECTS_TO_TEST:
                        resource, model, post_items, put_items, endpoints, \
                            user = get_sys_test_params(obj, 0, 'first',
                                                       'first')

                        parsed_model = model.parse_model()

                        if endpoints[0]:
                            item = post_items[0]
                            mod_item = put_items[0]

                            with self.subTest(resource, item=item,
                                              mod_item=mod_item, user=user):
                                # POST the item to the db and get the id.
                                result = c.post(f'/{endpoints[0]}',
                                                data=json.dumps(item),
                                                headers=self.get_headers(user))
                                _id = json.loads(result.data)['record']['id']

                                # PUT modified item.
                                result = c.put(f'/{endpoints[0]}/{_id}',
                                               data=json.dumps(mod_item),
                                               headers=self.get_headers(user))

                                record = json.loads(result.data)['record']

                                self.assertEqual(200, result.status_code)

                                self.check_record(mod_item, record,
                                                  parsed_model, item)

                                self.clear_db()
                                get_item_from_db.cache_clear()

    def test_put_without_authentication(self):
        """
        Test that PUT requests to a resource's endpoint return
        status code 401 if the user is not authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, _, put_items, endpoints, \
                        user = get_sys_test_params(obj, 0, 'none',
                                                   'first', 'fake')

                    if endpoints[0]:
                        mod_item = put_items[0]

                        with self.subTest(resource, mod_item=mod_item,
                                          user=user):
                            result = c.put(f'/{endpoints[0]}/999',
                                           data=json.dumps(mod_item),
                                           headers=self.get_headers(user))

                            self.assertEqual(401, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_put_not_unique(self):
        """
        Test that PUT requests to a resource's endpoint return
        status code 400 when violating a UNIQUE constraint.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, post_items,  put_items, endpoints, \
                        user = get_sys_test_params(obj, 0, 'all', 'all')

                    parsed_model = model.parse_model()

                    if endpoints[0] and parsed_model['unique']:
                        with self.subTest(resource, post_items=post_items,
                                          put_items=put_items, user=user):
                            # POST two items to the database and get the
                            # id of the second one.
                            c.post(f'/{endpoints[0]}',
                                   data=json.dumps(post_items[0]),
                                   headers=self.get_headers(user))

                            result = c.post(f'/{endpoints[0]}',
                                            data=json.dumps(post_items[1]),
                                            headers=self.get_headers(user))
                            _id = json.loads(result.data)['record']['id']

                            # PUT into second object data that violates
                            # unique contraint of the first object.
                            for item in put_items[1:]:
                                result = c.put(f'/{endpoints[0]}/{_id}',
                                               data=json.dumps(item),
                                               headers=self.get_headers(user))

                                self.assertEqual(400, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_put_not_found(self):
        """
        Test that PUT requests to a resource's endpoint return status
        code 404 if the record is not in the database.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, _, put_items, endpoints, \
                        user = get_sys_test_params(obj, 0, 'none', 'first')

                    if endpoints[0]:
                        mod_item = put_items[0]
                        with self.subTest(resource, mod_item=mod_item,
                                          user=user):
                            result = c.put(f'/{endpoints[0]}/999',
                                           data=json.dumps(mod_item),
                                           headers=self.get_headers(user))

                            self.assertEqual(404, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_delete_with_authentication(self):
        """
        Test that a DELETE requests to a resource's endpoint return
        status code 200 if the user is authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, post_items, _, endpoints, \
                        user = get_sys_test_params(obj, 0, 'first')

                    if endpoints[0]:
                        item = post_items[0]
                        with self.subTest(resource, item=item, user=user):
                            result = c.post(f'/{endpoints[0]}',
                                            data=json.dumps(item),
                                            headers=self.get_headers(user))
                            _id = json.loads(result.data)['record']['id']

                            result = c.delete(f'/{endpoints[0]}/{_id}',
                                              headers=self.get_headers(user))

                            self.assertEqual(200, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_delete_without_authentication(self):
        """
        Test that a DELETE requests to a resource's endpoint return
        status code 401 if the user is not authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, _, _, \
                        endpoints, user = get_sys_test_params(obj, 0, 'none',
                                                              'none', 'fake')

                    if endpoints[0]:
                        with self.subTest(resource, user=user):
                            result = c.delete(f'/{endpoints[0]}/999',
                                              headers=self.get_headers(user))

                            self.assertEqual(401, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_delete_not_found(self):
        """
        Test that a DELETE requests to a resource's endpoint return
        status code 404 if the record is not in the database.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, _, _, \
                        endpoints, user = get_sys_test_params(obj, 0)

                    if endpoints[0]:
                        with self.subTest(resource, user=user):
                            result = c.delete(f'/{endpoints[0]}/999',
                                              headers=self.get_headers(user))

                            self.assertEqual(404, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_activate_inactivate_with_authentication(self):
        """
        Test that PUT requests to the resource's endpoint with is_active=False
        and is_active=True toggle the is_active state for the record.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, post_items, _, \
                        endpoints, user = get_sys_test_params(obj, 1, 'first')

                    if endpoints[1]:
                        item = post_items[0]

                        with self.subTest(resource, item=item, user=user):
                            result = c.post(f'/{endpoints[0]}',
                                            data=json.dumps(item),
                                            headers=self.get_headers(user))
                            _id = json.loads(result.data)['record']['id']

                            # Make record inactive
                            result = c.put(f'/{endpoints[1]}/{_id}',
                                           data=json.dumps({
                                               'is_active': False
                                           }),
                                           headers=self.get_headers(user))

                            self.assertEqual(200, result.status_code)

                            self.assertEqual('El registro fue inactivado.',
                                             json.loads(
                                                 result.data)['message']
                                             )

                            # Make record active.
                            result = c.put(f'/{endpoints[1]}/{_id}',
                                           data=json.dumps({
                                               'is_active': True
                                           }),
                                           headers=self.get_headers(user))

                            self.assertEqual(200, result.status_code)

                            self.assertEqual('El registro fue activado.',
                                             json.loads(
                                                 result.data)['message']
                                             )

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_activate_inactivate_active_inactive(self):
        """
        Test that PUT requests to the resource's endpoint with is_active=True
        and is_active=False return status code 400 if the record is already
        active or inactive.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, post_items, _, \
                        endpoints, user = get_sys_test_params(obj, 1, 'first')

                    if endpoints[1]:
                        item = post_items[0]
                        with self.subTest(resource, item=item, user=user):
                            result = c.post(f'/{endpoints[0]}',
                                            data=json.dumps(item),
                                            headers=self.get_headers(user))
                            _id = json.loads(result.data)['record']['id']

                            # Try to activate an active record.
                            result = c.put(f'/{endpoints[1]}/{_id}',
                                           data=json.dumps({
                                               'is_active': True
                                           }),
                                           headers=self.get_headers(user))

                            self.assertEqual(400, result.status_code)

                            self.assertEqual('El registro ya estaba activo.',
                                             json.loads(
                                                 result.data)['message']
                                             )

                            # Make record inactive.
                            c.put(f'/{endpoints[1]}/{_id}',
                                  data=json.dumps({
                                      'is_active': False
                                  }),
                                  headers=self.get_headers(user))

                            # Try to inactivate an inactive record.
                            result = c.put(f'/{endpoints[1]}/{_id}',
                                           data=json.dumps({
                                               'is_active': False
                                           }),
                                           headers=self.get_headers(user))

                            self.assertEqual(400, result.status_code)

                            self.assertEqual('El registro ya estaba inactivo.',
                                             json.loads(
                                                 result.data)['message']
                                             )

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_activate_without_authentication(self):
        """
        Test that a PUT requests to the resource's endpoint return
        status code 401 if user is not authenticated.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, _, _, endpoints, \
                        user = get_sys_test_params(obj, 1, 'none',
                                                   'none', 'fake')

                    if endpoints[1]:
                        with self.subTest(resource, user=user):
                            result = c.put(f'/{endpoints[1]}/999',
                                           data=json.dumps({
                                               'is_active': True
                                           }),
                                           headers=self.get_headers(user))

                            self.assertEqual(401, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_activate_not_found(self):
        """
        Test that a PUT requests to the resource's endpoint return
        status code 404 if the record is not in the database.
        """
        with self.client() as c:
            with self.app_context():
                for obj in OBJECTS_TO_TEST:
                    resource, model, _, _, endpoints, \
                        user = get_sys_test_params(obj, 1, 'none', 'none')

                    if endpoints[1]:
                        with self.subTest(resource, user=user):
                            result = c.put(f'/{endpoints[1]}/999',
                                           data=json.dumps({
                                               'is_active': True
                                           }),
                                           headers=self.get_headers(user))

                            self.assertEqual(404, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_list_with_authentication(self):
        """
        Test that GET requests to the resource's endpoint return the list
        of records if the user is authenticated.
        """
        with self.client() as c:
            with self.app_context():
                objs = deepcopy(OBJECTS_TO_TEST)
                objs.append(RAW_ATTENDANCE)
                for obj in objs:
                    resource, model, post_items, _, endpoints, \
                        user = get_sys_test_params(obj, 2, 'first')

                    parsed_model = model.parse_model()

                    if endpoints[2]:
                        with self.subTest(resource, user=user):
                            # No need to post data for these endpoints.
                            if endpoints[2] in ['marital_statuses',
                                                'countries',
                                                'banks',
                                                'family_relations']:
                                result = c.get(f'/{endpoints[2]}',
                                               headers=self.get_headers(user))
                            else:
                                item = post_items[0]
                                if endpoints[2] == 'raw_attendances':
                                    item['auth_token'] = current_app.config[
                                        'CLOCK_SECRETS'][item['stgid']]
                                    _id = None
                                    c.post(f'/{endpoints[0]}',
                                           data=json.dumps(item),
                                           headers={
                                               'Content-Type':
                                                   'application/json',
                                               'Accept': 'application/text'
                                           })
                                else:
                                    item = post_items[0]
                                    c.post(f'/{endpoints[0]}',
                                           data=json.dumps(item),
                                           headers=self.get_headers(user))

                                    if 'schedule_id' in parsed_model['keys']:
                                        _id = item['schedule_id']
                                    elif 'payment_id' in parsed_model['keys']:
                                        _id = item['payment_id']
                                    elif 'employee_id' in parsed_model['keys']:
                                        _id = item['employee_id']
                                    elif 'uniform_item_id' in \
                                            parsed_model['keys']:
                                        _id = item['uniform_item_id']
                                    elif 'department_id' in \
                                            parsed_model['keys'] and \
                                            endpoints[2] is not 'employees':
                                        _id = item['department_id']
                                    else:
                                        _id = None

                                if _id:
                                    result = c.get(f'/{endpoints[2]}/{_id}',
                                                   headers=self.get_headers(
                                                       user))
                                else:
                                    result = c.get(f'/{endpoints[2]}',
                                                   headers=self.get_headers(
                                                       user))

                            _list = json.loads(result.data)['list']

                            self.assertEqual(200, result.status_code)

                            self.assertGreater(len(_list), 0)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_list_without_authentication(self):
        """
        Test that GET requests to the resource's endpoint return status
        code 401 if the user is not authenticated.
        """
        with self.client() as c:
            with self.app_context():
                objs = deepcopy(OBJECTS_TO_TEST)
                objs.append(RAW_ATTENDANCE)
                for obj in objs:
                    resource, model, _, _, endpoints, \
                        user = get_sys_test_params(obj, 2, 'none',
                                                   'none', 'fake')

                    if endpoints[2]:
                        with self.subTest(resource, user=user):
                            if endpoints[2] in ['absence_authorizations',
                                                'attendances', 'bank_accounts',
                                                'deduction_details',
                                                'deductions', 'dependents',
                                                'emergency_contacts',
                                                'employee', 'health_permits',
                                                'passports', 'payment_details',
                                                'payments', 'raw_attendance',
                                                'schedule_details',
                                                'schedules', 'sick_notes',
                                                'uniform_requirements',
                                                'uniform_sizes']:
                                result = c.get(f'/{endpoints[2]}/999',
                                               headers=self.get_headers(user))
                            else:
                                result = c.get(f'/{endpoints[2]}',
                                               headers=self.get_headers(user))

                            self.assertEqual(401, result.status_code)

                            self.clear_db()
                            get_item_from_db.cache_clear()

    def test_post_raw_attendance_with_authentication(self):
        """
        Test that a  POST request to the raw_attendance endpoint return
        status code 200 and 'ok' if the correct secret is included.
        """
        with self.client() as c:
            with self.app_context():
                resource, model, post_items, _, endpoints, \
                    user = get_sys_test_params(RAW_ATTENDANCE, 0, 'first')

                item = post_items[0]

                self.assertIsNone(
                    model.query.filter_by(**item).first())

                item['auth_token'] = current_app.config[
                    'CLOCK_SECRETS'][item['stgid']]

                result = c.post(f'/{endpoints[0]}',
                                data=json.dumps(item),
                                headers={
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/text'
                                })

                self.assertEqual(200, result.status_code)

                self.clear_db()
                get_item_from_db.cache_clear()

    def test_post_raw_attendance_without_authentication(self):
        """
        Test that a  POST request to the raw_attendance endpoint return
        status code 401 if the correct secret is not included.
        """
        with self.client() as c:
            with self.app_context():
                resource, model, post_items, _, endpoints, \
                    user = get_sys_test_params(RAW_ATTENDANCE, 0, 'first')

                item = post_items[0]

                self.assertIsNone(
                    model.query.filter_by(**item).first())

                item['auth_token'] = 'fAkEsEcReT'

                result = c.post(f'/{endpoints[0]}',
                                data=json.dumps(item),
                                headers={
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/text'
                                })

                self.assertEqual(401, result.status_code)

                self.clear_db()
                get_item_from_db.cache_clear()
