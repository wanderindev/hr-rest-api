from unittest import TestCase

from models.schedule import ScheduleModel


class TestSchedule(TestCase):
    """Unit tests for the ScheduleModel."""

    def test_init(self):
        """Test the __init__ method of the ScheduleModel class."""
        self.sch = ScheduleModel('test_sch', 1)

        self.assertEqual(self.sch.start_date, 'test_sch')
        self.assertEqual(self.sch.department_id, 1)
