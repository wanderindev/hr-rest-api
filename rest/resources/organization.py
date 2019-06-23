from models.organization import OrganizationModel
from resources.mixin import ActivateMixin, ListMixin, ResourceMixin


class Organization(ResourceMixin):
    model = OrganizationModel
    parsed_model = model.parse_model()


class ActivateOrganization(ActivateMixin):
    model = OrganizationModel


class Organizations(ListMixin):
    model = OrganizationModel
