from models.department import DepartmentModel
from models.schedule import ScheduleModel
from tests.base_test import BaseTest


class TestSchedule(BaseTest):
    """Integration tests for the ScheduleModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an
        organization, a department and a schedule.
        """
        super(TestSchedule, self).setUp()

        with self.app_context():
            self.o = self.get_organization()
            self.d = self.get_department(self.o.id)
            self.sch = self.get_schedule(self.d.id, self.o.id)

    def test_find_schedule(self):
        """Test the find_by_id method of ScheduleModel."""
        with self.app_context():
            sch_by_id = ScheduleModel.find_by_id(self.sch.id,
                                                 self.o.id)

            self.assertIsNotNone(sch_by_id)
