from models.creditor import CreditorModel
from resources.mixin import ActivateMixin, ListMixin, ResourceMixin


class Creditor(ResourceMixin):
    model = CreditorModel
    parsed_model = model.parse_model()


class ActivateCreditor(ActivateMixin):
    model = CreditorModel
    parsed_model = model.parse_model()


class Creditors(ListMixin):
    model = CreditorModel
