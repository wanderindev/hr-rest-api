from resources.mixin import ListMixin
from models.bank import BankModel


class Banks(ListMixin):
    model = BankModel
