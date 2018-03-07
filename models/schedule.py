from db import db
from models.department import DepartmentModel
from models.mixin import ModelMixin


class ScheduleModel(ModelMixin, db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    department_id = db.Column(db.Integer,
                              db.ForeignKey('department.id'),
                              nullable=False, index=True)

    def __init__(self, start_date, department_id):
        self.start_date = start_date
        self.department_id = department_id

    @classmethod
    def find_by_id(cls, _id, user):
        sch = cls.query.filter_by(id=_id).first()

        if sch:
            if DepartmentModel.find_by_id(sch.department_id, user):
                   return sch
