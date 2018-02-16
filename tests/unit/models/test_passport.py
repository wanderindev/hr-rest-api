from datetime import date
from unittest import TestCase

from models.passport import PassportModel


class TestPassport(TestCase):
    """Unit tests for the PassportModel."""

    def test_init(self):
        """Test the __init__ method of the PassportModel class."""
        self.p = PassportModel('123456', date(2018, 1, 1),
                               date(2019, 1, 1), 1, 1)

        self.assertEqual(self.p.passport_number, '123456')
        self.assertEqual(self.p.issue_date, date(2018, 1, 1))
        self.assertEqual(self.p.expiration_date, date(2019, 1, 1))
        self.assertEqual(self.p.employee_id, 1)
        self.assertEqual(self.p.country_id, 1)
