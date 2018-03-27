from unittest import TestCase

from models.payment_detail import PaymentDetailModel


class TestPaymentDetail(TestCase):
    """Unit tests for the PaymentDetailModel."""

    def test_init(self):
        """Test the __init__ method of the PaymentDetailModel class."""
        self.pmt_d = PaymentDetailModel('Salario Regular', 1234.56, 123.45,
                                        12.34, 1.23, 1)

        self.assertEqual(self.pmt_d.payment_type, 'Salario Regular')
        self.assertEqual(self.pmt_d.gross_payment, 1234.56)
        self.assertEqual(self.pmt_d.ss_deduction, 123.45)
        self.assertEqual(self.pmt_d.se_deduction, 12.34)
        self.assertEqual(self.pmt_d.isr_deduction, 1.23)
        self.assertEqual(self.pmt_d.payment_id, 1)
