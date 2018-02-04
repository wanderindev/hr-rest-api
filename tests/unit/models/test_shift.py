from datetime import time
from unittest import TestCase

from models.shift import ShiftModel


class TestShift(TestCase):
    """Unit tests for the ShiftModel."""
    def setUp(self):
        self.s_r = ShiftModel('test_s_r', 48, True, 'Quincenal',
                              time(0, 30), False, True, 1,
                              rotation_start_hour=time(6),
                              rotation_end_hour=time(21))

        print(self.s_r.break_length)

        self.s_f = ShiftModel('test_s_f', 44, False, 'Quincenal',
                              time(0, 30), False, True, 1,
                              fixed_start_hour_monday=time(8),
                              fixed_start_break_hour_monday=time(12),
                              fixed_end_break_hour_monday=time(12, 30),
                              fixed_end_hour_monday=time(16, 30),
                              fixed_start_hour_tuesday=time(8),
                              fixed_start_break_hour_tuesday=time(12),
                              fixed_end_break_hour_tuesday=time(12, 30),
                              fixed_end_hour_tuesday=time(16, 30),
                              fixed_start_hour_wednesday=time(8),
                              fixed_start_break_hour_wednesday=time(12),
                              fixed_end_break_hour_wednesday=time(12, 30),
                              fixed_end_hour_wednesday=time(16, 30),
                              fixed_start_hour_thursday=time(8),
                              fixed_start_break_hour_thursday=time(12),
                              fixed_end_break_hour_thursday=time(12, 30),
                              fixed_end_hour_thursday=time(16, 30),
                              fixed_start_hour_friday=time(8),
                              fixed_start_break_hour_friday=time(12),
                              fixed_end_break_hour_friday=time(12, 30),
                              fixed_end_hour_friday=time(16, 30),
                              fixed_start_hour_saturday=time(8),
                              fixed_end_hour_saturday=time(12),
                              rest_day='Domingo')

    def test_init_rotating(self):
        """
        Test the __init__ method of the ShiftModel
        class for rotating shift.
        """
        self.assertEqual(self.s_r.shift_name, 'test_s_r')

        self.assertEqual(self.s_r.weekly_hours, 48)

        self.assertEqual(self.s_r.is_rotating, True)

        self.assertEqual(self.s_r.payment_period, 'Quincenal')

        self.assertEqual(self.s_r.break_length, time(0, 30))

        self.assertEqual(self.s_r.is_break_included_in_shift, False)

        self.assertEqual(self.s_r.is_active, True)

        self.assertEqual(self.s_r.organization_id, 1)

        self.assertEqual(self.s_r.rotation_start_hour, time(6))

        self.assertEqual(self.s_r.rotation_end_hour, time(21))

    def test_init_fixed(self):
        """
        Test the __init__ method of the ShiftModel
        class for fixed shift.
        """
        self.assertEqual(self.s_f.shift_name, 'test_s_f')

        self.assertEqual(self.s_f.weekly_hours, 44)

        self.assertEqual(self.s_f.is_rotating, False)

        self.assertEqual(self.s_f.payment_period, 'Quincenal')

        self.assertEqual(self.s_f.break_length, time(0, 30))

        self.assertEqual(self.s_f.is_break_included_in_shift, False)

        self.assertEqual(self.s_f.is_active, True)

        self.assertEqual(self.s_f.organization_id, 1)

        self.assertEqual(self.s_f.fixed_start_hour_monday, time(8))

        self.assertEqual(self.s_f.fixed_start_break_hour_monday, time(12))

        self.assertEqual(self.s_f.fixed_end_break_hour_monday, time(12, 30))

        self.assertEqual(self.s_f.fixed_end_hour_monday, time(16, 30))

        self.assertEqual(self.s_f.fixed_start_hour_tuesday, time(8))

        self.assertEqual(self.s_f.fixed_start_break_hour_tuesday, time(12))

        self.assertEqual(self.s_f.fixed_end_break_hour_tuesday, time(12, 30))

        self.assertEqual(self.s_f.fixed_end_hour_tuesday, time(16, 30))

        self.assertEqual(self.s_f.fixed_start_hour_wednesday, time(8))

        self.assertEqual(self.s_f.fixed_start_break_hour_wednesday, time(12))

        self.assertEqual(self.s_f.fixed_end_break_hour_wednesday, time(12, 30))

        self.assertEqual(self.s_f.fixed_end_hour_wednesday, time(16, 30))

        self.assertEqual(self.s_f.fixed_start_hour_thursday, time(8))

        self.assertEqual(self.s_f.fixed_start_break_hour_thursday, time(12))

        self.assertEqual(self.s_f.fixed_end_break_hour_thursday, time(12, 30))

        self.assertEqual(self.s_f.fixed_end_hour_thursday, time(16, 30))

        self.assertEqual(self.s_f.fixed_start_hour_friday, time(8))

        self.assertEqual(self.s_f.fixed_start_break_hour_friday, time(12))

        self.assertEqual(self.s_f.fixed_end_break_hour_friday, time(12, 30))

        self.assertEqual(self.s_f.fixed_end_hour_friday, time(16, 30))

        self.assertEqual(self.s_f.fixed_start_hour_saturday, time(8))

        self.assertEqual(self.s_f.fixed_end_hour_saturday, time(12))

        self.assertIsNone(self.s_f.fixed_start_break_hour_saturday)

        self.assertIsNone(self.s_f.fixed_end_break_hour_saturday)

        self.assertIsNone(self.s_f.fixed_start_hour_sunday)

        self.assertIsNone(self.s_f.fixed_start_break_hour_sunday)

        self.assertIsNone(self.s_f.fixed_end_break_hour_sunday)

        self.assertIsNone(self.s_f.fixed_end_hour_sunday)

        self.assertEqual(self.s_f.rest_day, 'Domingo')
