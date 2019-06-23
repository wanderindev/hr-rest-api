from models.uniform_item import UniformItemModel
from resources.mixin import ListMixin, ResourceMixin


class UniformItem(ResourceMixin):
    model = UniformItemModel
    parsed_model = model.parse_model()


class UniformItems(ListMixin):
    model = UniformItemModel
