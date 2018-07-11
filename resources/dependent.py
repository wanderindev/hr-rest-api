from models.dependent import DependentModel
from resources.mixin import ListMixin, ResourceMixin


class Dependent(ResourceMixin):
    model = DependentModel
    parsed_model = model.parse_model()


class Dependents(ListMixin):
    model = DependentModel
