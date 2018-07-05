from unittest import TestCase

from models.uniform_size import UniformSizeModel


class TestUniformSize(TestCase):
    """Unit tests for the UniformSizeModel."""

    def test_init(self):
        """Test the __init__ method of the UniformSizeModel class."""
        self.u_i = UniformSizeModel('test_u_s', 1)

        self.assertEqual(self.u_i.size_description, 'test_u_s')
        self.assertEqual(self.u_i.uniform_item_id, 1)
