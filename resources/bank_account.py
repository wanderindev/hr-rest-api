from models.bank_account import BankAccountModel
from resources.mixin import ActivateMixin, ListMixin, ResourceMixin


class BankAccount(ResourceMixin):
    model = BankAccountModel
    parsed_model = model.parse_model()


class ActivateBankAccount(ActivateMixin):
    model = BankAccountModel


class BankAccounts(ListMixin):
    model = BankAccountModel
