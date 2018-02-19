from db import db
from models.mixin import ModelMixin
from models.uniform_item import UniformItemModel


class UniformRequirementModel(ModelMixin, db.Model):
    __tablename__ = 'uniform_requirement'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)
    uniform_item_id = db.Column(db.Integer,
                                db.ForeignKey('uniform_item.id'),
                                nullable=False, index=True)
    uniform_size_id = db.Column(db.Integer,
                                db.ForeignKey('uniform_size.id'),
                                nullable=False, index=True)

    def __init__(self, employee_id, uniform_item_id, uniform_size_id):
        self.employee_id = employee_id
        self.uniform_item_id = uniform_item_id
        self.uniform_size_id = uniform_size_id

    @classmethod
    def find_by_id(cls, _id, organization_id):
        req = cls.query.filter_by(id=_id).first()

        if req:
            if UniformItemModel.find_by_id(
                    req.uniform_item_id,
                    organization_id).organization_id == organization_id:
                return req
