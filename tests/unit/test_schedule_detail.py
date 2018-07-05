from datetime import datetime
from unittest import TestCase

from models.schedule_detail import ScheduleDetailModel


class TestScheduleDetail(TestCase):
    """Unit tests for the ScheduleDetailModel."""

    def test_init(self):
        """Test the __init__ method of the ScheduleDetailModel."""
        self.sch_d = ScheduleDetailModel(datetime(2018, 1, 1, 6, 0, 0),
                                         datetime(2018, 1, 1, 14, 0, 0),
                                         'comment 1',
                                         datetime(2018, 1, 2, 6, 0, 0),
                                         datetime(2018, 1, 2, 14, 0, 0),
                                         'comment 2',
                                         datetime(2018, 1, 3, 6, 0, 0),
                                         datetime(2018, 1, 3, 14, 0, 0),
                                         'comment 3',
                                         datetime(2018, 1, 4, 6, 0, 0),
                                         datetime(2018, 1, 4, 14, 0, 0),
                                         'comment 4',
                                         None,
                                         None,
                                         None,
                                         datetime(2018, 1, 6, 22, 0, 0),
                                         datetime(2018, 1, 7, 6, 0, 0),
                                         'comment 6',
                                         datetime(2018, 1, 7, 22, 0, 0),
                                         datetime(2018, 1, 8, 6, 0, 0),
                                         'comment 7',
                                         1,
                                         1)

        self.assertEqual(self.sch_d.day_1_start, datetime(2018, 1, 1, 6, 0, 0))
        self.assertEqual(self.sch_d.day_1_end, datetime(2018, 1, 1, 14, 0, 0))
        self.assertEqual(self.sch_d.day_1_comment, 'comment 1')
        self.assertEqual(self.sch_d.day_2_start, datetime(2018, 1, 2, 6, 0, 0))
        self.assertEqual(self.sch_d.day_2_end, datetime(2018, 1, 2, 14, 0, 0))
        self.assertEqual(self.sch_d.day_2_comment, 'comment 2')
        self.assertEqual(self.sch_d.day_3_start, datetime(2018, 1, 3, 6, 0, 0))
        self.assertEqual(self.sch_d.day_3_end, datetime(2018, 1, 3, 14, 0, 0))
        self.assertEqual(self.sch_d.day_3_comment, 'comment 3')
        self.assertEqual(self.sch_d.day_4_start, datetime(2018, 1, 4, 6, 0, 0))
        self.assertEqual(self.sch_d.day_4_end, datetime(2018, 1, 4, 14, 0, 0))
        self.assertEqual(self.sch_d.day_4_comment, 'comment 4')
        self.assertEqual(self.sch_d.day_5_start, None)
        self.assertEqual(self.sch_d.day_5_end, None)
        self.assertEqual(self.sch_d.day_5_comment, None)
        self.assertEqual(self.sch_d.day_6_start, datetime(2018, 1, 6, 22, 0, 0))
        self.assertEqual(self.sch_d.day_6_end, datetime(2018, 1, 7, 6, 0, 0))
        self.assertEqual(self.sch_d.day_6_comment, 'comment 6')
        self.assertEqual(self.sch_d.day_7_start, datetime(2018, 1, 7, 22, 0, 0))
        self.assertEqual(self.sch_d.day_7_end, datetime(2018, 1, 8, 6, 0, 0))
        self.assertEqual(self.sch_d.day_7_comment, 'comment 7')
