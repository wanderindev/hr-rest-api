from models.bank import BankModel
from models.bank_account import BankAccountModel
from models.employee import EmployeeModel
from tests.base_test import BaseTest


class TestBankAccount(BaseTest):
    """Integration tests for the BankAccountModel."""
    def setUp(self):
        """Extend the BaseTest setUp method by setting up a bank_account."""
        super(TestBankAccount, self).setUp()

        self.b_a = self.get_bank_account()

    def test_find_id(self):
        """Test the find_by_id methods of BankAccountModel."""
        with self.app_context():
            b_a = BankAccountModel.find_by_id(self.b_a.id,
                                              self.u)

            self.assertIsNotNone(b_a)

    def test_bank_accounts_list_in_employee(self):
        """
        Test that the employee object contains an
        bank_accounts list.
        """
        with self.app_context():
            employee_id = self.get_employee().id
            b_a_list = BankAccountModel.query.filter_by(
                employee_id=employee_id).all()
            b_a_list_in_employee = EmployeeModel.find_by_id(
                employee_id, self.u).bank_accounts

            self.assertListEqual(b_a_list, b_a_list_in_employee)

    def test_bank_accounts_list_in_bank(self):
        """
        Test that the bank object contains an
        bank_accounts list.
        """
        with self.app_context():
            b_a_list = BankAccountModel.query.filter_by(
                bank_id=1).all()
            b_a_list_in_bank = BankModel.query.filter_by(
                id=1).first().bank_accounts

            self.assertListEqual(b_a_list, b_a_list_in_bank)
