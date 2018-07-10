from models.emergency_contact import EmergencyContactModel
from resources.mixin import ActivateMixin, ListMixin, ResourceMixin


class EmergencyContact(ResourceMixin):
    model = EmergencyContactModel
    parsed_model = model.parse_model()


class EmergencyContacts(ListMixin):
    model = EmergencyContactModel