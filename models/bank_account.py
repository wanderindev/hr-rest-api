from db import db
from models.enum import ACCOUNT_TYPE
from models.mixin import ModelMixin


class BankAccountModel(ModelMixin, db.Model):
    __tablename__ = 'bank_account'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(50), nullable=False)
    account_type = db.Column(ACCOUNT_TYPE, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, index=True)
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)
    bank_id = db.Column(db.Integer,
                        db.ForeignKey('bank.id'),
                        nullable=False, index=True)

    def __init__(self, account_number, account_type,
                 is_active, employee_id, bank_id):
        self.account_number = account_number
        self.account_type = account_type
        self.is_active = is_active
        self.employee_id = employee_id
        self.bank_id = bank_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.employee import EmployeeModel

        b_acc = cls.query.filter_by(id=_id).first()

        if b_acc:
            if EmployeeModel.find_by_id(b_acc.employee_id, user):
                return b_acc
