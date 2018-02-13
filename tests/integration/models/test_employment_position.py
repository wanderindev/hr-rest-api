from models.employment_position import EmploymentPositionModel
from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestEmploymentPosition(BaseTest):
    """Integration tests for the EmploymentPositionModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating an organization and an
        employment position, saving them to the database, and getting their ids.
        """
        super(TestEmploymentPosition, self).setUp()

        with self.app_context():
            # Instantiate an organization, save it to the database,
            # and get its id.
            self.o = OrganizationModel('test_o', True)
            self.o.save_to_db()
            self.organization_id = self.o.id

            # Instantiate an employment position, save it to the database,
            # and get its id.
            self.e_p = EmploymentPositionModel('test_e_p_f', 'test_e_p_m',
                                               1.00, True, self.organization_id)
            self.e_p.save_to_db()
            self.position_id = self.e_p.id

    def test_find_employment_position(self):
        """
        Test the find_by_name and find_by_id methods of EmploymentPositionModel.
        """
        with self.app_context():
            e_p_by_name = EmploymentPositionModel.find_by_name(
                'test_e_p_f', self.organization_id)
            e_p_by_id = EmploymentPositionModel.find_by_id(
                self.position_id, self.organization_id)

            self.assertIsNotNone(e_p_by_name)
            self.assertIsNotNone(e_p_by_id)
            self.assertEqual(e_p_by_name, e_p_by_id)

    def test_employment_position_list_in_organization(self):
        """Test that the organization contains a employment_position list."""
        with self.app_context():
            e_p_list = EmploymentPositionModel.query .filter_by(
                organization_id=self.organization_id).all()
            o_e_p_list = OrganizationModel.find_by_name(
                'test_o').employment_positions

            self.assertListEqual(e_p_list, o_e_p_list)
