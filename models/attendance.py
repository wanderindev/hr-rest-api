from sqlalchemy import UniqueConstraint

from db import db
from models.mixin import ModelMixin


class ScheduleDetailModel(ModelMixin, db.Model):
    __tablename__ = 'attendance'
    __table_args__ = (UniqueConstraint('employee_id', 'schedule_id',
                                       name='attendance_employee_id_'
                                            'work_day_uindex'),)
    exclude_from_update = ('employee_id',)

    id = db.Column(db.Integer, primary_key=True)
    work_day = db.Column(db.Date, nullable=False)
    day_start = db.Column(db.DateTime)
    break_start = db.Column(db.DateTime)
    break_end = db.Column(db.DateTime)
    day_end = db.Column(db.DateTime)
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)

    def __init__(self, work_day, day_start, break_start, break_end,
                 day_end, employee_id):
        self.work_day = work_day
        self.day_start = day_start
        self.break_start = break_start
        self.break_end = break_end
        self.day_end = day_end
        self.employee_id = employee_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.employee import EmployeeModel

        record = cls.query.filter_by(id=_id).first()

        if record:
            if EmployeeModel.find_by_id(record.employee_id, user):
                return record

    @classmethod
    def find_all(cls, user, employee_id):
        from models.employee import EmployeeModel

        records = cls.query.filter_by(employee_id=employee_id).all()

        if records and EmployeeModel.find_by_id(employee_id, user):
            return records
