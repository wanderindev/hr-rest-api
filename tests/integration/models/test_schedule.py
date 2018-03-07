from models.department import DepartmentModel
from models.schedule import ScheduleModel
from tests.base_test import BaseTest


class TestSchedule(BaseTest):
    """Integration tests for the ScheduleModel."""
    def setUp(self):
        """Extend the BaseTest setUp method by setting up a schedule."""
        super(TestSchedule, self).setUp()

        with self.app_context():
            self.sch = self.get_schedule()

    def test_find_schedule(self):
        """Test the find_by_id method of ScheduleModel."""
        with self.app_context():
            sch = ScheduleModel.find_by_id(self.sch.id, self.u)

            self.assertIsNotNone(sch)
