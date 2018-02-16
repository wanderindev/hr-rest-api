from unittest import TestCase

from models.country import CountryModel


class TestCountry(TestCase):
    """Unit tests for the CountryModel."""

    def test_init(self):
        """Test the __init__ method of the CountryModel class."""
        self.c = CountryModel('Panamá', 'panameña')

        self.assertEqual(self.c.country_name, 'Panamá')
        self.assertEqual(self.c.nationality, 'panameña')
