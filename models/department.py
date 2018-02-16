from db import db
from models.employee import EmployeeModel
from models.mixin import ModelMixin


class DepartmentModel(ModelMixin, db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    organization_id = db.Column(db.Integer,
                                db.ForeignKey('organization.id'),
                                nullable=False, index=True)

    employees = db.relationship(EmployeeModel,
                                backref='department',
                                lazy='joined')

    def __init__(self, department_name, organization_id, is_active):
        self.department_name = department_name
        self.organization_id = organization_id
        self.is_active = is_active

    @classmethod
    def find_by_id(cls, _id, organization_id):
        return cls.query.filter_by(id=_id,
                                   organization_id=organization_id).first()

    @classmethod
    def find_by_name(cls, department_name, organization_id):
        return cls.query.filter_by(department_name=department_name,
                                   organization_id=organization_id).first()
