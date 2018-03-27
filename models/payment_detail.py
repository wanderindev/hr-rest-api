from db import db
from models.enum import PAYMENT_TYPE
from models.mixin import ModelMixin


class PaymentDetailModel(ModelMixin, db.Model):
    __tablename__ = 'payment_detail'

    id = db.Column(db.Integer, primary_key=True)
    payment_type = db.Column(PAYMENT_TYPE, nullable=False)
    gross_payment = db.Column(db.Numeric(7, 2), nullable=False)
    ss_deduction = db.Column(db.Numeric(7, 2))
    se_deduction = db.Column(db.Numeric(7, 2))
    isr_deduction = db.Column(db.Numeric(7, 2))
    payment_id = db.Column(db.Integer,
                           db.ForeignKey('payment.id'),
                           nullable=False, index=True)

    def __init__(self, payment_type, gross_payment, ss_deduction,
                 se_deduction, isr_deduction, payment_id):
        self.payment_type = payment_type
        self.gross_payment = gross_payment
        self.ss_deduction = ss_deduction
        self.se_deduction = se_deduction
        self.isr_deduction = isr_deduction
        self.payment_id = payment_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.payment import PaymentModel

        pmt_d = cls.query.filter_by(id=_id).first()

        if pmt_d:
            if PaymentModel.find_by_id(pmt_d.payment_id, user):
                return pmt_d
