from models.country import CountryModel
from tests.base_test import BaseTest


class TestCountry(BaseTest):
    """Integration tests for the CountryModel."""
    def test_find_all(self):
        """Test the find_all method of CountryModel."""
        with self.app_context():
            c_list = CountryModel.find_all()

            self.assertIsNotNone(c_list)
            self.assertTrue(len(c_list) > 0)
