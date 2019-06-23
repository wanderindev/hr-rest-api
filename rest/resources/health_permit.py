from models.health_permit import HealthPermitModel
from resources.mixin import ListMixin, ResourceMixin


class HealthPermit(ResourceMixin):
    model = HealthPermitModel
    parsed_model = model.parse_model()


class HealthPermits(ListMixin):
    model = HealthPermitModel
