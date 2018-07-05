from datetime import date
from unittest import TestCase

from models.health_permit import HealthPermitModel


class TestHealthPermit(TestCase):
    """Unit tests for the HealthPermitModel."""

    def test_init(self):
        """Test the __init__ method of the HealthPermitModel class."""
        self.h_p = HealthPermitModel('Verde', date(2018, 1, 1),
                                     date(2019, 1, 1), 1)

        self.assertEqual(self.h_p.health_permit_type, 'Verde')
        self.assertEqual(self.h_p.issue_date, date(2018, 1, 1))
        self.assertEqual(self.h_p.expiration_date, date(2019, 1, 1))
        self.assertEqual(self.h_p.employee_id, 1)
