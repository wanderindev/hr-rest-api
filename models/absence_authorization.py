from sqlalchemy import UniqueConstraint

from db import db
from models.mixin import ModelMixin


class AbsenceAuthorizationModel(ModelMixin, db.Model):
    __tablename__ = 'absence_authorization'
    __table_args__ = (UniqueConstraint('employee_id', 'absence_date',
                                       name='absence_authorization_employee_id'
                                            '_absence_date_uindex'),)
    exclude_from_update = ('employee_id',)

    id = db.Column(db.Integer, primary_key=True)
    absence_date = db.Column(db.Date, nullable=False)
    absence_reason = db.Column(db.String(40))
    is_payment_authorized = db.Column(db.Boolean, nullable=False,
                                      default=False)
    authorization_request_date = db.Column(db.Date, nullable=False)
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)

    def __init__(self, absence_date, absence_reason, is_payment_authorized,
                 authorization_request_date, employee_id):
        self.absence_date = absence_date
        self.absence_reason = absence_reason
        self.is_payment_authorized = is_payment_authorized
        self.authorization_request_date = authorization_request_date
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
