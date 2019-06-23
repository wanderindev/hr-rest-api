from sqlalchemy import UniqueConstraint

from db import db
from models.enum import ACCOUNT_TYPE
from models.mixin import ModelMixin


class BankAccountModel(ModelMixin, db.Model):
    __tablename__ = 'bank_account'
    __table_args__ = (UniqueConstraint('account_number', 'employee_id',
                                       'bank_id',
                                       name='bank_account_account_number_'
                                            'employee_id_bank_id_uindex'),)
    exclude_from_update = ('employee_id',)

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
