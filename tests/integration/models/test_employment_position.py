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
        self.e_p = self.get_employment_position(self.o.id)

    def test_find_employment_position(self):
        """
        Test the find_by_name and find_by_id
        methods of EmploymentPositionModel.
        """
        with self.app_context():
            e_p_by_name = EmploymentPositionModel.find_by_name(
                self.e_p.position_name_feminine, self.o.id)
            e_p_by_id = EmploymentPositionModel.find_by_id(
                self.e_p.id, self.o.id)

            self.assertIsNotNone(e_p_by_name)
            self.assertIsNotNone(e_p_by_id)
            self.assertEqual(e_p_by_name, e_p_by_id)

    def test_employment_position_list_in_organization(self):
        """Test that the organization contains a employment_position list."""
        with self.app_context():
            e_p_list = EmploymentPositionModel.query .filter_by(
                organization_id=self.o.id).all()
            o_e_p_list = OrganizationModel.find_by_name(
                self.o.organization_name).employment_positions

            self.assertListEqual(e_p_list, o_e_p_list)
