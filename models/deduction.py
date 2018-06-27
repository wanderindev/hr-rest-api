from db import db
from models.enum import PAYMENT_METHOD
from models.mixin import ModelMixin


class DeductionModel(ModelMixin, db.Model):
    __tablename__ = 'deduction'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    deduction_per_payment_period = db.Column(db.Numeric(7, 2), nullable=False)
    payment_method = db.Column(PAYMENT_METHOD, nullable=False)
    deduct_in_december = db.Column(db.Boolean, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)
    creditor_id = db.Column(db.Integer,
                            db.ForeignKey('creditor.id'),
                            nullable=False, index=True)

    def __init__(self, start_date, end_date, deduction_per_payment_period,
                 payment_method, deduct_in_december, is_active,
                 employee_id, creditor_id):
        self.start_date = start_date
        self.end_date = end_date
        self.deduction_per_payment_period = deduction_per_payment_period
        self.payment_method = payment_method
        self.deduct_in_december = deduct_in_december
        self.is_active = is_active
        self.employee_id = employee_id
        self.creditor_id = creditor_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.employee import EmployeeModel

        ded = cls.query.filter_by(id=_id).first()

        if ded:
            if EmployeeModel.find_by_id(ded.employee_id, user):
                return ded
