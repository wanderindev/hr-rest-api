from sqlalchemy import UniqueConstraint

from db import db
from models.mixin import ModelMixin


class UniformSizeModel(ModelMixin, db.Model):
    __tablename__ = 'uniform_size'
    __table_args__ = (UniqueConstraint('size_description', 'uniform_item_id',
                                       name='uniform_size_size_description_uniform_item_id_uindex'),)

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

        record = cls.query.filter_by(id=_id).first()

        if record:
            if UniformItemModel.find_by_id(record.uniform_item_id, user):
                return record

    @classmethod
    def find_all(cls, user, item_id):
        from models.uniform_item import UniformItemModel

        records = cls.query.filter_by(uniform_item_id=item_id).all()

        if records and UniformItemModel.find_by_id(item_id, user):
            return records
