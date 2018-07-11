from models.family_relation import FamilyRelationModel
from resources.mixin import ActivateMixin, ListMixin, ResourceMixin


class FamilyRelations(ListMixin):
    model = FamilyRelationModel

