from models.department import DepartmentModel
from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestDepartment(BaseTest):
    """Integration tests for the DepartmentModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by instantiating an organization and a
        department, saving them to the database, and getting their ids.
        """
        super(TestDepartment, self).setUp()

        with self.app_context():
            # Instantiate an organization, save it to the database,
            # and get its id.
            self.o = OrganizationModel('test_o', True)
            self.o.save_to_db()
            self.organization_id = self.o.id

            # Instantiate a department, save it to the database,
            # and get its id.
            self.d = DepartmentModel('test_d', self.organization_id, True)
            self.d.save_to_db()
            self.department_id = self.d.id

    def test_find_department(self):
        """Test the find_by_name and find_by_id methods of DepartmentModel."""
        with self.app_context():
            d_by_name = DepartmentModel.find_by_name('test_d',
                                                     self.organization_id)
            d_by_id = DepartmentModel.find_by_id(self.department_id,
                                                 self.organization_id)

            self.assertIsNotNone(d_by_name)
            self.assertIsNotNone(d_by_name)
            self.assertEqual(d_by_name, d_by_id)

    def test_department_list_in_organization(self):
        """Test that the organization object contains a department list."""
        with self.app_context():
            d_list = DepartmentModel.query.filter_by(
                organization_id=self.organization_id).all()
            o_d_list = OrganizationModel.find_by_name('test_o').departments

            self.assertListEqual(d_list, o_d_list)
