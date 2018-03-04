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
            self.d = self.get_department()

    def test_find_department(self):
        """Test the find_by_id method of DepartmentModel."""
        with self.app_context():
            d = DepartmentModel.find_by_id(self.d.id,
                                           self.u)

            self.assertIsNotNone(d)

    def test_department_list_in_organization(self):
        """Test that the organization object contains a department list."""
        with self.app_context():
            dept_list = DepartmentModel.query.filter_by(
                organization_id=self.o.id).all()
            dept_list_in_org = OrganizationModel.find_by_id(self.o.id,
                                                            self.u).departments

            self.assertListEqual(dept_list, dept_list_in_org)
