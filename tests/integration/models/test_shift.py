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
        self.u = self.get_user(self.o.id)
        self.s = self.get_shift(self.u)

    def test_find_shift(self):
        """Test the find_by_id method of ShiftModel."""
        with self.app_context():
            shift = ShiftModel.find_by_id(self.s.id, self.u)

            self.assertIsNotNone(shift)

    def test_shift_list_in_organization(self):
        """Test that the organization object contains a shift list."""
        with self.app_context():
            s_list = ShiftModel.query.filter_by(
                organization_id=self.o.id).all()
            s_list_in_org = OrganizationModel.find_by_id(
                self.o.id, self.u).shifts

            self.assertListEqual(s_list, s_list_in_org)
