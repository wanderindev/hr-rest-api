from models.bank import BankModel
from tests.base_test import BaseTest


class TestBank(BaseTest):
    """Integration tests for the BankModel."""
    def test_find_all(self):
        """Test the find_all method of BankModel."""
        with self.app_context():
            b_list = BankModel.find_all()

            self.assertIsNotNone(b_list)
            self.assertTrue(len(b_list) > 0)
