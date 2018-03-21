from models.schedule import ScheduleModel
from models.schedule_detail import ScheduleDetailModel
from tests.base_test import BaseTest


class TestScheduleDetail(BaseTest):
    """Integration tests for the ScheduleDetailModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up a schedule detail.
        """
        super(TestScheduleDetail, self).setUp()

        self.sch_d = self.get_schedule_detail()

    def test_find_schedule_detail(self):
        """Test the find_by_id method of ScheduleDetailModel."""
        with self.app_context():
            sch_d = ScheduleDetailModel.find_by_id(self.sch_d.id, self.u)

            self.assertIsNotNone(sch_d)

    def test_schedule_detail_list_in_schedule(self):
        """Test that the schedule object contains a schedule detail list."""
        with self.app_context():
            sch_d_list = ScheduleDetailModel.query.filter_by(
                schedule_id=self.sch_d.schedule_id).all()
            sch_d_list_in_sch = ScheduleModel.find_by_id(
                self.sch_d.schedule_id, self.u).schedule_details

            self.assertListEqual(sch_d_list, sch_d_list_in_sch)
