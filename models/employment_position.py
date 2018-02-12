from sqlalchemy import and_, or_
from db import db
from models.mixin import ModelsMixin


class EmploymentPositionModel(ModelsMixin, db.Model):
    __tablename__ = 'employment_position'

    id = db.Column(db.Integer, primary_key=True)
    position_name_feminine = db.Column(db.String(80), nullable=False)
    position_name_masculine = db.Column(db.String(80), nullable=False)
    minimum_hourly_wage = db.Column(db.Numeric(8, 4))
    is_active = db.Column(db.Boolean, nullable=False)
    organization_id = db.Column(db.Integer,
                                db.ForeignKey('organization.id'),
                                nullable=False, index=True)

    employees = db.relationship('EmployeeModel',
                                backref='employment_position',
                                lazy='joined')

    def __init__(self, position_name_feminine, position_name_masculine,
                 minimum_hourly_wage,  is_active, organization_id):
        self.position_name_feminine = position_name_feminine
        self.position_name_masculine = position_name_masculine
        self.minimum_hourly_wage = minimum_hourly_wage
        self.is_active = is_active
        self.organization_id = organization_id

    @classmethod
    def find_by_id(cls, _id, organization_id):
        return cls.query.filter_by(id=_id,
                                   organization_id=organization_id).first()

    @classmethod
    def find_by_name(cls, position_name, organization_id):
        return cls.query.filter(and_(
            or_(cls.position_name_feminine == position_name,
                cls.position_name_masculine == position_name),
            cls.organization_id == organization_id)).first()
