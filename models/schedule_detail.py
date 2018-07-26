from sqlalchemy import UniqueConstraint

from db import db
from models.mixin import ModelMixin


class ScheduleDetailModel(ModelMixin, db.Model):
    __tablename__ = 'schedule_detail'
    __table_args__ = (UniqueConstraint('employee_id', 'schedule_id',
                                       name='schedule_detail_employee_id_'
                                            'schedule_id_uindex'),)
    exclude_from_update = ('schedule_id')

    id = db.Column(db.Integer, primary_key=True)
    day_1_start = db.Column(db.DateTime)
    day_1_end = db.Column(db.DateTime)
    day_1_comment = db.Column(db.String(40))
    day_2_start = db.Column(db.DateTime)
    day_2_end = db.Column(db.DateTime)
    day_2_comment = db.Column(db.String(40))
    day_3_start = db.Column(db.DateTime)
    day_3_end = db.Column(db.DateTime)
    day_3_comment = db.Column(db.String(40))
    day_4_start = db.Column(db.DateTime)
    day_4_end = db.Column(db.DateTime)
    day_4_comment = db.Column(db.String(40))
    day_5_start = db.Column(db.DateTime)
    day_5_end = db.Column(db.DateTime)
    day_5_comment = db.Column(db.String(40))
    day_6_start = db.Column(db.DateTime)
    day_6_end = db.Column(db.DateTime)
    day_6_comment = db.Column(db.String(40))
    day_7_start = db.Column(db.DateTime)
    day_7_end = db.Column(db.DateTime)
    day_7_comment = db.Column(db.String(40))
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)
    schedule_id = db.Column(db.Integer,
                            db.ForeignKey('schedule.id'),
                            nullable=False, index=True)

    def __init__(self, day_1_start, day_1_end, day_1_comment, day_2_start,
                 day_2_end, day_2_comment, day_3_start, day_3_end,
                 day_3_comment, day_4_start, day_4_end, day_4_comment,
                 day_5_start, day_5_end, day_5_comment, day_6_start, day_6_end,
                 day_6_comment, day_7_start, day_7_end, day_7_comment,
                 employee_id, schedule_id):
        self.day_1_start = day_1_start
        self.day_1_end = day_1_end
        self.day_1_comment = day_1_comment
        self.day_2_start = day_2_start
        self.day_2_end = day_2_end
        self.day_2_comment = day_2_comment
        self.day_3_start = day_3_start
        self.day_3_end = day_3_end
        self.day_3_comment = day_3_comment
        self.day_4_start = day_4_start
        self.day_4_end = day_4_end
        self.day_4_comment = day_4_comment
        self.day_5_start = day_5_start
        self.day_5_end = day_5_end
        self.day_5_comment = day_5_comment
        self.day_6_start = day_6_start
        self.day_6_end = day_6_end
        self.day_6_comment = day_6_comment
        self.day_7_start = day_7_start
        self.day_7_end = day_7_end
        self.day_7_comment = day_7_comment
        self.employee_id = employee_id
        self.schedule_id = schedule_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.employee import EmployeeModel

        record = cls.query.filter_by(id=_id).first()

        if record:
            if EmployeeModel.find_by_id(record.employee_id, user):
                return record

    @classmethod
    def find_all(cls, user, schedule_id):
        from models.schedule import ScheduleModel

        records = cls.query.filter_by(schedule_id=schedule_id).all()

        if records and ScheduleModel.find_by_id(schedule_id, user):
            return records
