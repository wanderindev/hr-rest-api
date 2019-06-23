from models.uniform_size import UniformSizeModel
from resources.mixin import ListMixin, ResourceMixin


class UniformSize(ResourceMixin):
    model = UniformSizeModel
    parsed_model = model.parse_model()


class UniformSizes(ListMixin):
    model = UniformSizeModel
