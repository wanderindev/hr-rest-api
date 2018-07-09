from models.employment_position import EmploymentPositionModel
from resources.mixin import ActivateMixin, ListMixin, ResourceMixin


class EmploymentPosition(ResourceMixin):
    model = EmploymentPositionModel
    parsed_model = model.parse_model()


class ActivateEmploymentPosition(ActivateMixin):
    model = EmploymentPositionModel


class EmploymentPositions(ListMixin):
    model = EmploymentPositionModel
