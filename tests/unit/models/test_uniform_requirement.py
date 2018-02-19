from unittest import TestCase

from models.uniform_requirement import UniformRequirementModel


class TestUniformRequirement(TestCase):
    """Unit tests for the UniformRequirementModel."""

    def test_init(self):
        """Test the __init__ method of the UniformRequirementModel class."""
        self.u_r = UniformRequirementModel(1, 1, 1)

        self.assertEqual(self.u_r.employee_id, 1)
        self.assertEqual(self.u_r.uniform_item_id, 1)
        self.assertEqual(self.u_r.uniform_size_id, 1)
