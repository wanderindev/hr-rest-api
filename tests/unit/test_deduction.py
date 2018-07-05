from datetime import date
from unittest import TestCase

from models.deduction import DeductionModel


class TestDeduction(TestCase):
    """Unit tests for the DeductionModel."""

    def test_init(self):
        """Test the __init__ method of the DeductionModel class."""
        self.ded = DeductionModel(date(2018, 1, 1),
                                  date(2018, 1, 31),
                                  123.45,
                                  'Cheque',
                                  True,
                                  True,
                                  1,
                                  1)

        self.assertEqual(self.ded.start_date, date(2018, 1, 1))
        self.assertEqual(self.ded.end_date, date(2018, 1, 31))
        self.assertEqual(self.ded.deduction_per_payment_period, 123.45)
        self.assertEqual(self.ded.payment_method, 'Cheque')
        self.assertTrue(self.ded.deduct_in_december)
        self.assertTrue(self.ded.is_active, date(2018, 1, 1))
        self.assertEqual(self.ded.employee_id, 1)
        self.assertEqual(self.ded.creditor_id, 1)
