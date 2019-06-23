from models.absence_authorization import AbsenceAuthorizationModel
from resources.mixin import ListMixin, ResourceMixin


class AbsenceAuthorization(ResourceMixin):
    model = AbsenceAuthorizationModel
    parsed_model = model.parse_model()


class AbsenceAuthorizations(ListMixin):
    model = AbsenceAuthorizationModel
