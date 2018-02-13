from unittest import TestCase

from models.employment_position import EmploymentPositionModel


class TestEmploymentPosition(TestCase):
    """Unit tests for the EmploymentPositionModel."""

    def test_init(self):
        """Test the __init__ method of the EmploymentPositionModel class."""
        self.e_p = EmploymentPositionModel('test_e_p_f', 'test_e_p_m',
                                           1.00, True, 1)

        self.assertEqual(self.e_p.position_name_feminine, 'test_e_p_f')
        self.assertEqual(self.e_p.position_name_masculine, 'test_e_p_m')
        self.assertEqual(self.e_p.minimum_hourly_wage, 1.00)
        self.assertEqual(self.e_p.is_active, True)
        self.assertEqual(self.e_p.organization_id, 1)
