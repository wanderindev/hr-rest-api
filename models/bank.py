from db import db
from models.mixin import ModelMixin
from models.bank_account import BankAccountModel


class BankModel(ModelMixin, db.Model):
    __tablename__ = 'bank'
    exclude_from_update = ()

    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(80), nullable=False)

    bank_accounts = db.relationship(BankAccountModel,
                                    backref='bank',
                                    lazy='joined')

    def __init__(self, bank_name):
        self.bank_name = bank_name

    @classmethod
    def find_all(cls, user):
        return cls.query.order_by('bank_name').all()
