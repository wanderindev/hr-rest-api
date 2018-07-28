from db import db
from models.mixin import ModelMixin


class FamilyRelationModel(ModelMixin, db.Model):
    __tablename__ = 'family_relation'
    exclude_from_update = ()

    id = db.Column(db.Integer, primary_key=True)
    relation_feminine = db.Column(db.String(25), nullable=False)
    relation_masculine = db.Column(db.String(25), nullable=False)

    def __init__(self, relation_feminine, relation_masculine):
        self.relation_feminine = relation_feminine
        self.relation_masculine = relation_masculine

    @classmethod
    def find_all(cls, _):
        return cls.query.order_by('relation_feminine').all()
