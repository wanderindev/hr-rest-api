from models.creditor import CreditorModel
from models.deduction import DeductionModel
from models.employee import EmployeeModel
from tests.base_test import BaseTest


class TestDeduction(BaseTest):
    """Integration tests for the DeductionModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an employee,
        aa creditor, and a deduction.
        """
        super(TestDeduction, self).setUp()

        self.e = self.get_employee()
        self.cr = self.get_creditor()
        self.ded = self.get_deduction()

    def test_find_id(self):
        """Test the find_by_id method of DeductionModel."""
        with self.app_context():
            ded = DeductionModel.find_by_id(self.ded.id, self.u)

            self.assertIsNotNone(ded)

    def test_deduction_list_in_employee(self):
        """ Test that the employee object contains an deductions list. """
        with self.app_context():
            ded_list = DeductionModel.query.filter_by(
                employee_id=self.e.id).all()
            ded_list_in_employee = EmployeeModel.find_by_id(
                self.e.id, self.u).deductions

            self.assertListEqual(ded_list, ded_list_in_employee)

    def test_deduction_list_in_creditor(self):
        """ Test that the creditor object contains an deductions list. """
        with self.app_context():
            ded_list = DeductionModel.query.filter_by(
                creditor_id=self.cr.id).all()
            ded_list_in_creditor = CreditorModel.find_by_id(
                self.cr.id, self.u).deductions

            self.assertListEqual(ded_list, ded_list_in_creditor)
