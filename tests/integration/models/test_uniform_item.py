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
            self.u_i = self.get_uniform_item(self.o.id)

    def test_find_uniform_item(self):
        """Test the find_by_name and find_by_id methods of UniformItemModel."""
        with self.app_context():
            u_i_by_name = UniformItemModel.find_by_name(self.u_i.item_name,
                                                        self.o.id)
            u_i_by_id = UniformItemModel.find_by_id(self.u_i.id,
                                                    self.o.id)

            self.assertIsNotNone(u_i_by_name)
            self.assertIsNotNone(u_i_by_id)
            self.assertEqual(u_i_by_name, u_i_by_id)

    def test_uniform_item_list_in_organization(self):
        """Test that the organization object contains a uniform item list."""
        with self.app_context():
            u_i_list = UniformItemModel.query.filter_by(
                organization_id=self.o.id).all()
            o_u_i_list = OrganizationModel.find_by_name(
                self.o.organization_name).uniform_items

            self.assertListEqual(u_i_list, o_u_i_list)
