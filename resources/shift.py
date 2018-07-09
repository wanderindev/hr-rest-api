from models.shift import ShiftModel
from resources.mixin import ActivateMixin, ListMixin, ResourceMixin


class Shift(ResourceMixin):
    model = ShiftModel
    parsed_model = model.parse_model()


class ActivateShift(ActivateMixin):
    model = ShiftModel


class Shifts(ListMixin):
    model = ShiftModel
