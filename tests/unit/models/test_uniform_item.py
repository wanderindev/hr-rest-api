from unittest import TestCase

from models.uniform_item import UniformItemModel


class TestUniformItem(TestCase):
    """Unit tests for the UniformItemModel."""

    def test_init(self):
        """Test the __init__ method of the UniformItemModel class."""
        self.u_i = UniformItemModel('test_u_i', 1)

        self.assertEqual(self.u_i.item_name, 'test_u_i')
        self.assertEqual(self.u_i.organization_id, 1)
