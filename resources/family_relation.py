from models.family_relation import FamilyRelationModel
from resources.mixin import ListMixin


class FamilyRelations(ListMixin):
    model = FamilyRelationModel
