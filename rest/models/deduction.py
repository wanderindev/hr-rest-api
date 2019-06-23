from db import db
from models.deduction_detail import DeductionDetailModel
from models.enum import PAYMENT_METHOD
from models.mixin import ModelMixin


class DeductionModel(ModelMixin, db.Model):
    __tablename__ = 'deduction'
    exclude_from_update = ('employee_id', 'is_active')

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

    deduction_details = db.relationship(DeductionDetailModel,
                                        backref='deduction',
                                        lazy='joined')

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
