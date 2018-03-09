from models.organization import OrganizationModel
from models.uniform_item import UniformItemModel
from tests.base_test import BaseTest


class TestUniformItem(BaseTest):
    """Integration tests for the UniformItemModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an
        organization and a uniform item.
        """
        super(TestUniformItem, self).setUp()

        with self.app_context():
            self.o = self.get_organization()
            self.u_i = self.get_uniform_item()

    def test_find_uniform_item(self):
        """Test the find_by_name and find_by_id methods of UniformItemModel."""
        with self.app_context():
            u_i = UniformItemModel.find_by_id(self.u_i.id, self.u)

            self.assertIsNotNone(u_i)

    def test_uniform_item_list_in_organization(self):
        """Test that the organization object contains a uniform item list."""
        with self.app_context():
            u_i_list = UniformItemModel.query.filter_by(
                organization_id=self.o.id).all()
            u_i_list_in_org = OrganizationModel.find_by_id(
                self.o.id, self.u).uniform_items

            self.assertListEqual(u_i_list, u_i_list_in_org)
