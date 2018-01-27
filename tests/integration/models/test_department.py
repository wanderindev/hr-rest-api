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
        self.d = DepartmentModel('test_d', 1)

    def test_find_department(self):
        """
        Test the find_by_id, find_by_name, and find_by_organization_id
        methods of the DepartmentModel class.
        """
        with self.app_context():
            self.o.save_to_db()
            self.d.organization_id = OrganizationModel.find_by_name('test_o').id
            self.d.save_to_db()

            d_by_id = DepartmentModel.find_by_id(self.d.id)
            d_by_name = DepartmentModel.find_by_name(self.d.department_name,
                                                     self.d.organization_id)
            d_by_o_id = DepartmentModel.find_by_organization_id(
                self.d.organization_id)[0]

            self.assertIsNotNone(d_by_id)

            self.assertIsNotNone(d_by_name)

            self.assertIsNotNone(d_by_o_id)

            self.assertEqual(d_by_id, d_by_name)

            self.assertEqual(d_by_id, d_by_o_id)

    def test_department_list_in_organization(self):
        """Test that the org object contains a department list."""
        with self.app_context():
            self.o.save_to_db()
            self.d.organization_id = OrganizationModel.find_by_name('test_o').id
            self.d.save_to_db()

            d_list = DepartmentModel.find_by_organization_id(self.o.id)
            o_d_list = OrganizationModel.\
                find_by_name(self.o.organization_name).departments

            self.assertListEqual(d_list, o_d_list)
