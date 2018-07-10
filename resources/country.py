from resources.mixin import ListMixin
from models.country import CountryModel


class Countries(ListMixin):
    model = CountryModel
