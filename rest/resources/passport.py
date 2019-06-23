from models.passport import PassportModel
from resources.mixin import ListMixin, ResourceMixin


class Passport(ResourceMixin):
    model = PassportModel
    parsed_model = model.parse_model()

class Passports(ListMixin):
    model = PassportModel
