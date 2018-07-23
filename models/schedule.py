from sqlalchemy import UniqueConstraint

from db import db
from models.department import DepartmentModel
from models.schedule_detail import ScheduleDetailModel
from models.mixin import ModelMixin


class ScheduleModel(ModelMixin, db.Model):
    __tablename__ = 'schedule'
    __table_args__ = (UniqueConstraint('department_id', 'start_date',
                                       name='schedule_department_id_'
                                            'start_date_uindex'),)
    exclude_from_update = ('department_id',)

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    department_id = db.Column(db.Integer,
                              db.ForeignKey('department.id'),
                              nullable=False, index=True)

    schedule_details = db.relationship(ScheduleDetailModel,
                                       backref='schedule',
                                       lazy='joined')

    def __init__(self, start_date, department_id):
        self.start_date = start_date
        self.department_id = department_id

    @classmethod
    def find_by_id(cls, _id, user):
        record = cls.query.filter_by(id=_id).first()

        if record:
            if DepartmentModel.find_by_id(record.department_id, user):
                return record

    @classmethod
    def find_all(cls, user, department_id):
        from models.department import DepartmentModel

        records = cls.query.filter_by(department_id=department_id).all()

        if records and DepartmentModel.find_by_id(department_id, user):
            return records
