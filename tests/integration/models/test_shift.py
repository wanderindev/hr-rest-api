from models.shift import ShiftModel
from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestShift(BaseTest):
    """Integration tests for the ShiftModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an
        organization and a shift.
        """
        super(TestShift, self).setUp()

        self.o = self.get_organization()
        self.s = self.get_shift(self.o.id)

    def test_find_shift(self):
        """Test the find_by_name and find_by_id methods of ShiftModel."""
        with self.app_context():
            s_by_name = ShiftModel.find_by_name(self.s.shift_name,
                                                self.o.id)
            s_by_id = ShiftModel.find_by_id(self.s.id,
                                            self.o.id)

            self.assertIsNotNone(s_by_name)
            self.assertIsNotNone(s_by_id)
            self.assertEqual(s_by_name, s_by_id)

    def test_shift_list_in_organization(self):
        """Test that the organization object contains a shift list."""
        with self.app_context():
            s_list = ShiftModel.query.filter_by(
                organization_id=self.o.id).all()
            o_s_list = OrganizationModel.find_by_name(
                self.o.organization_name).shifts

            self.assertListEqual(s_list, o_s_list)
