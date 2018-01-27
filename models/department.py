from db import db
from models.mixin import ModelsMixin


class DepartmentModel(ModelsMixin, db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(80), nullable=False)
    organization_id = db.Column(db.Integer,
                                db.ForeignKey('organization.id'),
                                nullable=False, index=True)

    def __init__(self, department_name, organization_id):
        self.department_name = department_name
        self.organization_id = organization_id

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, department_name, organization_id):
        return cls.query.filter_by(department_name=department_name,
                                   organization_id=organization_id).first()

    @classmethod
    def find_by_organization_id(cls, _id):
        return cls.query.filter_by(organization_id=_id).order_by(cls.id).all()
