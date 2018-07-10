from models.uniform_requirement import UniformRequirementModel
from resources.mixin import ListMixin, ResourceMixin


class UniformRequirement(ResourceMixin):
    model = UniformRequirementModel
    parsed_model = model.parse_model()


class UniformRequirements(ListMixin):
    model = UniformRequirementModel
