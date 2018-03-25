from models.employee import EmployeeModel
from models.payment import PaymentModel
from tests.base_test import BaseTest


class TestPayment(BaseTest):
    """Integration tests for the PaymentModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an employee
        and a payment.
        """
        super(TestPayment, self).setUp()

        self.e = self.get_employee()
        self.pmt = self.get_payment()

    def test_find_id(self):
        """Test the find_by_id method of PaymentModel."""
        with self.app_context():
            pmt = PaymentModel.find_by_id(self.pmt.id, self.u)

            self.assertIsNotNone(pmt)

    def test_payment_list_in_employee(self):
        """ Test that the employee object contains an payment list. """
        with self.app_context():
            pmt_list = PaymentModel.query.filter_by(
                employee_id=self.e.id).all()
            pmt_list_in_employee = EmployeeModel.find_by_id(
                self.e.id, self.u).payments

            self.assertListEqual(pmt_list, pmt_list_in_employee)
