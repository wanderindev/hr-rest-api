from datetime import time

from models.shift import ShiftModel
from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestShift(BaseTest):
    """Integration tests for the ShiftModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating
        an OrganizationModel object and a ShiftModel
        object before each test
        """
        super(TestShift, self).setUp()
        self.o = OrganizationModel('test_o', True)
        self.s = ShiftModel('test_s_r', 48, True, 'Quincenal',
                            time(0, 30), False, True, 1,
                            rotation_start_hour=time(6),
                            rotation_end_hour=time(21))

    def test_find_shift(self):
        """
        Test the find_by_name method of ShiftModel.
        """
        with self.app_context():
            self.o.save_to_db()
            self.s.organization_id = OrganizationModel.find_by_name('test_o').id
            self.s.save_to_db()

            s_by_name = ShiftModel.find_by_name('test_s_r',
                                                self.s.organization_id)

            self.assertIsNotNone(s_by_name)

    def test_shift_list_in_organization(self):
        """Test that the org object contains a shift list."""
        with self.app_context():
            self.o.save_to_db()
            self.s.organization_id = OrganizationModel.find_by_name('test_o').id
            self.s.save_to_db()

            s_list = ShiftModel.query.filter_by(organization_id=self.o.id).all()
            o_s_list = OrganizationModel.find_by_name('test_o').shifts

            self.assertListEqual(s_list, o_s_list)
