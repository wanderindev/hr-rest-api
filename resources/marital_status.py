from resources.mixin import ListMixin
from models.marital_status import MaritalStatusModel


class MaritalStatuses(ListMixin):
    model = MaritalStatusModel
