from models.user import AppUserModel
from resources.mixin import ActivateMixin, ListMixin, ResourceMixin


class User(ResourceMixin):
    model = AppUserModel
    parsed_model = model.parse_model()


class ActivateUser(ActivateMixin):
    model = AppUserModel


class Users(ListMixin):
    model = AppUserModel
