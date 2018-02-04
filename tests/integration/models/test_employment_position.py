from models.employment_position import EmploymentPositionModel
from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestEmploymentPosition(BaseTest):
    """Integration tests for the EmploymentPositionModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating
        an OrganizationModel object and a EmploymentPositionModel
        object before each test
        """
        super(TestEmploymentPosition, self).setUp()
        self.o = OrganizationModel('test_o', True)
        self.e_p = EmploymentPositionModel('test_e_p_f', 'test_e_p_m',
                                           1.00, True, 1)

    def test_find_employment_position(self):
        """
        Test the find_by_name method of EmploymentPositionModel.
        """
        with self.app_context():
            self.o.save_to_db()
            self.e_p.organization_id = OrganizationModel\
                .find_by_name('test_o').id
            self.e_p.save_to_db()

            e_p_by_name = EmploymentPositionModel\
                .find_by_name('test_e_p_f',
                              self.e_p.organization_id)

            self.assertIsNotNone(e_p_by_name)

            e_p_by_name = EmploymentPositionModel \
                .find_by_name('test_e_p_m',
                              self.e_p.organization_id)

            self.assertIsNotNone(e_p_by_name)

    def test_employment_position_list_in_organization(self):
        """Test that the org object contains a employment_position list."""
        with self.app_context():
            self.o.save_to_db()
            self.e_p.organization_id = OrganizationModel\
                .find_by_name('test_o').id
            self.e_p.save_to_db()

            e_p_list = EmploymentPositionModel.query\
                .filter_by(organization_id=self.o.id).all()
            o_e_p_list = OrganizationModel.find_by_name('test_o')\
                .employment_positions

            self.assertListEqual(e_p_list, o_e_p_list)