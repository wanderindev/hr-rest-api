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
            self.u_i = self.get_uniform_item()
            self.u_s = self.get_uniform_size()

    def test_find_uniform_size(self):
        """Test the find_by_id method of UniformSizeModel."""
        with self.app_context():
            u_s = UniformSizeModel.find_by_id(self.u_s.id, self.u)

            self.assertIsNotNone(u_s)

    def test_uniform_size_list_in_uniform_item(self):
        """Test that the uniform_item object contains a uniform size list."""
        with self.app_context():
            u_s_list = UniformSizeModel.query.filter_by(
                uniform_item_id=self.u_i.id).all()
            u_s_list_in_item = UniformItemModel.find_by_id(
                self.u_i.id, self.u).uniform_sizes

            self.assertListEqual(u_s_list, u_s_list_in_item)
