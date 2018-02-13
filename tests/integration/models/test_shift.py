from datetime import time

from models.shift import ShiftModel
from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestShift(BaseTest):
    """Integration tests for the ShiftModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating an organization and a
        shift, saving them to the database, and getting their ids.
        """
        super(TestShift, self).setUp()

        with self.app_context():
            # Instantiate an organization, save it to the database,
            # and get its id.
            self.o = OrganizationModel('test_o', True)
            self.o.save_to_db()
            self.organization_id = self.o.id

            # Instantiate a shift, save it to the database,
            # and get its id.
            self.s = ShiftModel('test_s_r', 48, True, 'Quincenal',
                                time(0, 30), False, True, self.organization_id,
                                rotation_start_hour=time(6),
                                rotation_end_hour=time(21))
            self.s.save_to_db()
            self.shift_id = self.s.id

    def test_find_shift(self):
        """Test the find_by_name and find_by_id methods of ShiftModel."""
        with self.app_context():
            s_by_name = ShiftModel.find_by_name('test_s_r',
                                                self.organization_id)
            s_by_id = ShiftModel.find_by_id(self.shift_id,
                                            self.organization_id)

            self.assertIsNotNone(s_by_name)
            self.assertIsNotNone(s_by_id)
            self.assertEqual(s_by_name, s_by_id)

    def test_shift_list_in_organization(self):
        """Test that the organization object contains a shift list."""
        with self.app_context():
            s_list = ShiftModel.query.filter_by(
                organization_id=self.organization_id).all()
            o_s_list = OrganizationModel.find_by_name('test_o').shifts

            self.assertListEqual(s_list, o_s_list)
