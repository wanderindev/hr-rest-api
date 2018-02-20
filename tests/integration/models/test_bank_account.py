from models.bank_account import BankAccountModel
from models.employee import EmployeeModel
from tests.base_test import BaseTest


class TestBankAccount(BaseTest):
    """Integration tests for the BankAccountModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an organization,
        a department, an employment position, a shift, an employee,
        and a bank_account.
        """
        super(TestBankAccount, self).setUp()

        self.o = self.get_organization()
        self.d = self.get_department(self.o.id)
        self.e_p = self.get_employment_position(self.o.id)
        self.s = self.get_shift(self.o.id)
        self.e = self.get_employee(self.d.id, self.e_p.id, self.s.id, self.o.id)
        self.b_a = self.get_bank_account('1234', 'Corriente',
                                         True, self.e.id, 1, self.o.id)

    def test_find_id(self):
        """Test the find_by_id methods of BankAccountModel."""
        with self.app_context():
            b_a = BankAccountModel.find_by_id(self.b_a.id,
                                              self.o.id)

            self.assertIsNotNone(b_a)

    def test_bank_accounts_list_in_employee(self):
        """
        Test that the employee object contains an
        bank_accounts list.
        """
        with self.app_context():
            b_a_list = BankAccountModel.query.filter_by(
                employee_id=self.e.id).all()
            e_b_a_list = EmployeeModel.find_by_id(
                self.e.id, self.o.id).bank_accounts

            self.assertListEqual(b_a_list, e_b_a_list)
