from models.department import DepartmentModel
from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestDepartment(BaseTest):
    """Integration tests for the DepartmentModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating
        an OrganizationModel object and a DepartmentModel
        object before each test
        """
        super(TestDepartment, self).setUp()
        self.o = OrganizationModel('test_o', True)
        self.d = DepartmentModel('test_d', 1, True)

    def test_find_department(self):
        """
        Test the find_by_name and find_by_id
        methods of DepartmentModel.
        """
        with self.app_context():
            self.o.save_to_db()
            self.d.organization_id = OrganizationModel.find_by_name('test_o').id
            self.d.save_to_db()

            d_by_name = DepartmentModel.find_by_name('test_d',
                                                     self.d.organization_id)

            d_by_id = DepartmentModel.find_by_id(self.d.id,
                                                 self.d.organization_id)

            self.assertIsNotNone(d_by_name)

            self.assertIsNotNone(d_by_name)

            self.assertEqual(d_by_name, d_by_id)

    def test_department_list_in_organization(self):
        """Test that the org object contains a department list."""
        with self.app_context():
            self.o.save_to_db()
            self.d.organization_id = OrganizationModel.find_by_name('test_o').id
            self.d.save_to_db()

            d_list = DepartmentModel.query\
                .filter_by(organization_id=self.o.id).all()
            o_d_list = OrganizationModel\
                .find_by_name('test_o').departments

            self.assertListEqual(d_list, o_d_list)
