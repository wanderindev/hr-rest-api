from unittest import TestCase

from models.deduction_detail import DeductionDetailModel


class TestDeductionDetail(TestCase):
    """Unit tests for the DeductionDetailModel."""

    def test_init(self):
        """Test the __init__ method of the DeductionDetailModel class."""
        self.d_d = DeductionDetailModel(67.89, 1, 1)

        self.assertEqual(self.d_d.deducted_amount, 67.89)
        self.assertEqual(self.d_d.payment_id, 1)
        self.assertEqual(self.d_d.deduction_id, 1)
