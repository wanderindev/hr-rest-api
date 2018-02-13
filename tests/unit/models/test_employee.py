from datetime import date
from unittest import TestCase

from models.employee import EmployeeModel


class TestEmployee(TestCase):
    """Unit tests for the EmployeeModel."""

    def test_init(self):
        """Test the __init__ method of the EmployeeModel class."""
        self.e = EmployeeModel('f_n', 's_n', 'f_sn', 's_sn', '1-11-111', True,
                               date(2000, 1, 31), 'Hombre', 'Panamá',
                               '222-2222', '6666-6666', 'f_n@f_sn.com',
                               'Definido', date(2018, 1, 1), date(2018, 1, 31),
                               date(2018, 1, 15), 'Período de Prueba', 104.00,
                               0, 'ACH', True, 1, 1, 1, 1)

        self.assertEqual(self.e.first_name, 'f_n')
        self.assertEqual(self.e.second_name, 's_n')
        self.assertEqual(self.e.first_surname, 'f_sn')
        self.assertEqual(self.e.second_surname, 's_sn')
        self.assertEqual(self.e.national_id_number, '1-11-111')
        self.assertEqual(self.e.is_panamanian, True)
        self.assertEqual(self.e.date_of_birth, date(2000, 1, 31))
        self.assertEqual(self.e.gender, 'Hombre')
        self.assertEqual(self.e.address, 'Panamá')
        self.assertEqual(self.e.home_phone, '222-2222')
        self.assertEqual(self.e.mobile_phone, '6666-6666')
        self.assertEqual(self.e.email, 'f_n@f_sn.com')
        self.assertEqual(self.e.type_of_contract, 'Definido')
        self.assertEqual(self.e.employment_date, date(2018, 1, 1))
        self.assertEqual(self.e.contract_expiration_date, date(2018, 1, 31))
        self.assertEqual(self.e.termination_date, date(2018, 1, 15))
        self.assertEqual(self.e.termination_reason, 'Período de Prueba')
        self.assertEqual(self.e.salary_per_payment_period, 104.00)
        self.assertEqual(self.e.representation_expenses_per_payment_period, 0)
        self.assertEqual(self.e.payment_method, 'ACH')
        self.assertEqual(self.e.is_active, True)
        self.assertEqual(self.e.marital_status_id, 1)
        self.assertEqual(self.e.department_id, 1)
        self.assertEqual(self.e.position_id, 1)
        self.assertEqual(self.e.shift_id, 1)
