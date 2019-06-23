from copy import deepcopy
from unittest import TestCase

from werkzeug.security import check_password_hash

from tests.business_objects import get_unit_test_params, OBJECTS_TO_TEST, \
    RAW_ATTENDANCE


class TestModels(TestCase):
    """Unit tests for the application models."""

    def check_assertions(self, expected, result):
        """Assert that all attributes of the result match the expected value"""
        for k, v in expected.items():
            if k == 'password':
                self.assertTrue(check_password_hash(
                    getattr(result, 'password_hash'), v))
            else:
                self.assertEquals(getattr(result, k), v)

    def test_init(self):
        """Test the __init__ method of the models."""
        objs = deepcopy(OBJECTS_TO_TEST)
        objs.append(RAW_ATTENDANCE)

        for obj in objs:
            model, item = get_unit_test_params(obj)

            with self.subTest(model.__tablename__):
                inst = model(**item)

                self.check_assertions(item, inst)
