from models.employment_position import EmploymentPositionModel
from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestEmploymentPosition(BaseTest):
    """Integration tests for the EmploymentPositionModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating an
        organization and an employment position.
        """
        super(TestEmploymentPosition, self).setUp()

        self.o = self.get_organization()
        self.e_p = self.get_employment_position()

    def test_find_employment_position(self):
        """Test the find_by_idmethod of EmploymentPositionModel."""
        with self.app_context():
            e_p = EmploymentPositionModel.find_by_id(self.e_p.id, self.u)

            self.assertIsNotNone(e_p)

    def test_employment_position_list_in_organization(self):
        """Test that the organization contains a employment_position list."""
        with self.app_context():
            e_p_list = EmploymentPositionModel.query .filter_by(
                organization_id=self.o.id).all()
            e_p_list_in_org = OrganizationModel.find_by_id(
                self.o.id, self.u).employment_positions

            self.assertListEqual(e_p_list, e_p_list_in_org)
