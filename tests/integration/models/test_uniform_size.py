from models.uniform_item import UniformItemModel
from models.uniform_size import UniformSizeModel
from tests.base_test import BaseTest


class TestUniformSize(BaseTest):
    """Integration tests for the UniformSizeModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an
        organization, a uniform item and a uniform size.
        """
        super(TestUniformSize, self).setUp()

        with self.app_context():
            self.o = self.get_organization()
            self.u_i = self.get_uniform_item(self.o.id)
            self.u_s = self.get_uniform_size(self.u_i.id, self.o.id)

    def test_find_uniform_size(self):
        """
        Test the find_by_description and find_by_id
        methods of UniformSizeModel.
        """
        with self.app_context():
            u_s_by_desc = UniformSizeModel.find_by_description(
                self.u_s.size_description, self.u_s.uniform_item_id, self.o.id)
            u_s_by_id = UniformSizeModel.find_by_id(self.u_s.id, self.o.id)

            self.assertIsNotNone(u_s_by_desc)
            self.assertIsNotNone(u_s_by_id)
            self.assertEqual(u_s_by_desc, u_s_by_id)

    def test_uniform_size_list_in_uniform_item(self):
        """Test that the uniform_item object contains a uniform size list."""
        with self.app_context():
            u_s_list = UniformSizeModel.query.filter_by(
                uniform_item_id=self.u_i.id).all()
            ui_u_s_list = UniformItemModel.find_by_name(
                self.u_i.item_name,
                self.o.id).uniform_sizes

            self.assertListEqual(u_s_list, ui_u_s_list)
