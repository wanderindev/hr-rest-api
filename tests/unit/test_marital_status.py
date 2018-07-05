from unittest import TestCase

from models.marital_status import MaritalStatusModel


class TestMaritalStatus(TestCase):
    """Unit tests for the MaritalStatusModel."""

    def test_init(self):
        """Test the __init__ method of the MaritalStatusModel class."""
        self.ms = MaritalStatusModel('marital_status_f', 'marital_status_m')

        self.assertEqual(self.ms.status_feminine, 'marital_status_f')
        self.assertEqual(self.ms.status_masculine, 'marital_status_m')
