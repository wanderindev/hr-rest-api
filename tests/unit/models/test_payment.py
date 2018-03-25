from datetime import date
from unittest import TestCase

from models.payment import PaymentModel


class TestPayment(TestCase):
    """Unit tests for the PaymentModel."""

    def test_init(self):
        """Test the __init__ method of the PaymentModel class."""
        self.pmt = PaymentModel(date(2018, 1, 1), '1234-abc', 1)

        self.assertEqual(self.pmt.payment_date, date(2018, 1, 1))
        self.assertEqual(self.pmt.document_number, '1234-abc')
        self.assertEqual(self.pmt.employee_id, 1)
