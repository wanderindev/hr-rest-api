from datetime import date
from unittest import TestCase

from models.dependent import DependentModel


class TestDependent(TestCase):
    """Unit tests for the DependentModel."""

    def test_init(self):
        """Test the __init__ method of the DependentModel class."""
        self.depen = DependentModel('f_n', 's_n', 'f_sn', 's_sn', 'Mujer',
                                    date(2018, 1, 1), 1, 1)

        self.assertEqual(self.depen.first_name, 'f_n')
        self.assertEqual(self.depen.second_name, 's_n')
        self.assertEqual(self.depen.first_surname, 'f_sn')
        self.assertEqual(self.depen.second_surname, 's_sn')
        self.assertEqual(self.depen.gender, 'Mujer')
        self.assertEqual(self.depen.date_of_birth, date(2018, 1, 1))
        self.assertEqual(self.depen.employee_id, 1)
        self.assertEqual(self.depen.family_relation_id, 1)
