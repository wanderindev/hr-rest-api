from db import db
from models.mixin import ModelMixin


class DeductionDetailModel(ModelMixin, db.Model):
    __tablename__ = 'deduction_detail'

    id = db.Column(db.Integer, primary_key=True)
    deducted_amount = db.Column(db.Numeric(7, 2), nullable=False)
    payment_id = db.Column(db.Integer,
                           db.ForeignKey('payment.id'),
                           nullable=False, index=True)
    deduction_id = db.Column(db.Integer,
                             db.ForeignKey('deduction.id'),
                             nullable=False, index=True)

    def __init__(self, deducted_amount, payment_id, deduction_id):
        self.deducted_amount = deducted_amount
        self.payment_id = payment_id
        self.deduction_id = deduction_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.deduction import DeductionModel

        d_d = cls.query.filter_by(id=_id).first()

        if d_d:
            if DeductionModel.find_by_id(d_d.deduction_id, user):
                return d_d
