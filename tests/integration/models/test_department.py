from models.department import DepartmentModel
from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestDepartment(BaseTest):
    """Integration tests for the DepartmentModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an
        organization and a department.
        """
        super(TestDepartment, self).setUp()

        with self.app_context():
            self.o = self.get_organization()
            self.d = self.get_department(self.o.id)

    def test_find_department(self):
        """Test the find_by_name and find_by_id methods of DepartmentModel."""
        with self.app_context():
            d_by_name = DepartmentModel.find_by_name(self.d.department_name,
                                                     self.o.id)
            d_by_id = DepartmentModel.find_by_id(self.d.id,
                                                 self.o.id)

            self.assertIsNotNone(d_by_name)
            self.assertIsNotNone(d_by_name)
            self.assertEqual(d_by_name, d_by_id)

    def test_department_list_in_organization(self):
        """Test that the organization object contains a department list."""
        with self.app_context():
            d_list = DepartmentModel.query.filter_by(
                organization_id=self.o.id).all()
            o_d_list = OrganizationModel.find_by_name(
                self.o.organization_name).departments

            self.assertListEqual(d_list, o_d_list)
