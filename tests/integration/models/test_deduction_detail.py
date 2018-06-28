from models.deduction import DeductionModel
from models.deduction_detail import DeductionDetailModel
from models.payment import PaymentModel
from tests.base_test import BaseTest


class TestDeductionDetail(BaseTest):
    """Integration tests for the DeductionDetailModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a payment,
        a deduction, and a deduction detail.
        """
        super(TestDeductionDetail, self).setUp()

        self.pmt = self.get_payment()
        self.ded = self.get_deduction()
        self.d_d = self.get_deduction_detail()

    def test_find_id(self):
        """Test the find_by_id method of DeductionDetailModel."""
        with self.app_context():
            d_d = DeductionDetailModel.find_by_id(self.d_d.id, self.u)

            self.assertIsNotNone(d_d)

    def test_deduction_detail_list_in_payment(self):
        """ Test that the payment object contains an deduction detail list. """
        with self.app_context():
            d_d_list = DeductionDetailModel.query.filter_by(
                payment_id=self.pmt.id).all()
            d_d_list_in_pmt = PaymentModel.find_by_id(
                self.pmt.id, self.u).deduction_details

            self.assertListEqual(d_d_list, d_d_list_in_pmt)

    def test_deduction_detail_list_in_deduction(self):
        """
        Test that the deduction object contains an deduction detail list.

        """
        with self.app_context():
            d_d_list = DeductionDetailModel.query.filter_by(
                deduction_id=self.ded.id).all()
            d_d_list_in_d = DeductionModel.find_by_id(
                self.ded.id, self.u).deduction_details

            self.assertListEqual(d_d_list, d_d_list_in_d)
