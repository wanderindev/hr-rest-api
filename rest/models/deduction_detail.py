from db import db
from models.mixin import ModelMixin


class DeductionDetailModel(ModelMixin, db.Model):
    __tablename__ = 'deduction_detail'
    exclude_from_update = ('deduction_id',)

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

        record = cls.query.filter_by(id=_id).first()

        if record:
            if DeductionModel.find_by_id(record.deduction_id, user):
                return record

    @classmethod
    def find_all(cls, user, payment_id):
        from models.payment import PaymentModel

        records = cls.query.filter_by(payment_id=payment_id).all()

        if records and PaymentModel.find_by_id(payment_id, user):
            return records
