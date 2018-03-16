from db import db
from models.mixin import ModelMixin


class UniformSizeModel(ModelMixin, db.Model):
    __tablename__ = 'uniform_size'

    id = db.Column(db.Integer, primary_key=True)
    size_description = db.Column(db.String(20), nullable=False)
    uniform_item_id = db.Column(db.Integer,
                                db.ForeignKey('uniform_item.id'),
                                nullable=False, index=True)

    def __init__(self, size_description, uniform_item_id):
        self.size_description = size_description
        self.uniform_item_id = uniform_item_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.uniform_item import UniformItemModel

        size = cls.query.filter_by(id=_id).first()

        if size:
            if UniformItemModel.find_by_id(size.uniform_item_id, user):
                return size
