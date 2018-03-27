from db import db
from models.mixin import ModelMixin
from models.payment_detail import PaymentDetailModel


class PaymentModel(ModelMixin, db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    payment_date = db.Column(db.Date, nullable=False)
    document_number = db.Column(db.String(40), nullable=False)
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)

    payment_details = db.relationship(PaymentDetailModel,
                                      backref='payment',
                                      lazy='joined')

    def __init__(self, payment_date, document_number, employee_id):
        self.payment_date = payment_date
        self.document_number = document_number
        self.employee_id = employee_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.employee import EmployeeModel

        pmt = cls.query.filter_by(id=_id).first()

        if pmt:
            if EmployeeModel.find_by_id(pmt.employee_id, user):
                return pmt
