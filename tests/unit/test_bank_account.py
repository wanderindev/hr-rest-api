from unittest import TestCase

from models.bank_account import BankAccountModel


class TestBankAccount(TestCase):
    """Unit tests for the BankAccountModel."""

    def test_init(self):
        """Test the __init__ method of the BankAccountModel class."""
        self.b_a = BankAccountModel('1234', 'Corriente', True, 1, 1)

        self.assertEqual(self.b_a.account_number, '1234')
        self.assertEqual(self.b_a.account_type, 'Corriente')
        self.assertEqual(self.b_a.is_active, True)
        self.assertEqual(self.b_a.employee_id, 1)
        self.assertEqual(self.b_a.bank_id, 1)
