from unittest import TestCase

from models.bank import BankModel


class TestBank(TestCase):
    """Unit tests for the BankModel."""

    def test_init(self):
        """Test the __init__ method of the BankModel class."""
        self.b = BankModel('test_b')

        self.assertEqual(self.b.bank_name, 'test_b')
