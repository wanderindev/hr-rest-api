from db import db
from models.enum import HEALTH_PERMIT_TYPE
from models.mixin import ModelMixin


class HealthPermitModel(ModelMixin, db.Model):
    __tablename__ = 'health_permit'

    id = db.Column(db.Integer, primary_key=True)
    health_permit_type = db.Column(HEALTH_PERMIT_TYPE, nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)

    def __init__(self, health_permit_type, issue_date,
                 expiration_date, employee_id):
        self.health_permit_type = health_permit_type
        self.issue_date = issue_date
        self.expiration_date = expiration_date
        self.employee_id = employee_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.employee import EmployeeModel

        h_permit = cls.query.filter_by(id=_id).first()

        if h_permit:
            if EmployeeModel.find_by_id(h_permit.employee_id, user):
                return h_permit
