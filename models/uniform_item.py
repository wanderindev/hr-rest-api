from db import db
from models.mixin import ModelMixin
from models.uniform_size import UniformSizeModel


class UniformItemModel(ModelMixin, db.Model):
    __tablename__ = 'uniform_item'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80), nullable=False)
    organization_id = db.Column(db.Integer,
                                db.ForeignKey('organization.id'),
                                nullable=False, index=True)

    uniform_sizes = db.relationship(UniformSizeModel,
                                    backref='uniform_item',
                                    lazy='joined')

    def __init__(self, item_name, organization_id):
        self.item_name = item_name
        self.organization_id = organization_id

    @classmethod
    def find_by_id(cls, _id, organization_id):
        return cls.query.filter_by(id=_id,
                                   organization_id=organization_id).first()

    @classmethod
    def find_by_name(cls, item_name, organization_id):
        return cls.query.filter_by(item_name=item_name,
                                   organization_id=organization_id).first()