from models.payment import PaymentModel
from models.payment_detail import PaymentDetailModel
from tests.base_test import BaseTest


class TestPaymentDetail(BaseTest):
    """Integration tests for the PaymentDetailModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a payment
        and a payment detail.
        """
        super(TestPaymentDetail, self).setUp()

        self.pmt = self.get_payment()
        self.pmt_d = self.get_payment_detail()

    def test_find_id(self):
        """Test the find_by_id method of PaymentDetailModel."""
        with self.app_context():
            pmt_d = PaymentDetailModel.find_by_id(self.pmt_d.id, self.u)

            self.assertIsNotNone(pmt_d)

    def test_payment_detail_list_in_payment(self):
        """ Test that the payment object contains an payment detail list. """
        with self.app_context():
            pmt_d_list = PaymentDetailModel.query.filter_by(
                payment_id=self.pmt_d.payment_id).all()
            pmt_d_list_in_pmt = PaymentModel.find_by_id(
                self.pmt.id, self.u).payment_details

            self.assertListEqual(pmt_d_list, pmt_d_list_in_pmt)
