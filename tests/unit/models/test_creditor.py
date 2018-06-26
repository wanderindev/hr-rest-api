from unittest import TestCase

from models.creditor import CreditorModel


class TestCreditor(TestCase):
    """Unit tests for the CreditorModel."""

    def test_init(self):
        """Test the __init__ method of the CreditorModel class."""
        self.cr = CreditorModel('test_cr', '123-4567', 'test@test_cr.com',
                                1, True)

        self.assertEqual(self.cr.creditor_name, 'test_cr')
        self.assertEqual(self.cr.phone_number, '123-4567')
        self.assertEqual(self.cr.email, 'test@test_cr.com')
        self.assertEqual(self.cr.organization_id, 1)
        self.assertTrue(self.cr.is_active)
