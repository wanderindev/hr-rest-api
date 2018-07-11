from models.deduction import DeductionModel
from resources.mixin import ActivateMixin, ListMixin, ResourceMixin


class Deduction(ResourceMixin):
    model = DeductionModel
    parsed_model = model.parse_model()


class ActivateDeduction(ActivateMixin):
    model = DeductionModel


class Deductions(ListMixin):
    model = DeductionModel
