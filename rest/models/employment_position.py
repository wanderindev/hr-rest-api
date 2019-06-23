from sqlalchemy import UniqueConstraint

from db import db
from models.employee import EmployeeModel
from models.mixin import ModelMixin


class EmploymentPositionModel(ModelMixin, db.Model):
    __tablename__ = 'employment_position'
    __table_args__ = (UniqueConstraint('position_name_feminine',
                                       'organization_id',
                                       name='employment_position_'
                                            'p_name_feminine_'
                                            'organization_id_uindex'),
                      UniqueConstraint('position_name_masculine',
                                       'organization_id',
                                       name='employment_position_'
                                            'p_name_masculine_'
                                            'organization_id_uindex')
                      )
    exclude_from_update = ('organization_id', 'is_active')

    id = db.Column(db.Integer, primary_key=True)
    position_name_feminine = db.Column(db.String(80), nullable=False)
    position_name_masculine = db.Column(db.String(80), nullable=False)
    minimum_hourly_wage = db.Column(db.Numeric(8, 4))
    is_active = db.Column(db.Boolean, nullable=False)
    organization_id = db.Column(db.Integer,
                                db.ForeignKey('organization.id'),
                                nullable=False, index=True)

    employees = db.relationship(EmployeeModel,
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
    def find_by_id(cls, _id, user):
        from models.organization import OrganizationModel

        record = cls.query.filter_by(id=_id).first()

        if record:
            if OrganizationModel.find_by_id(record.organization_id, user):
                return record

    @classmethod
    def find_all(cls, user):
        return cls.query.filter_by(organization_id=user.organization_id).all()
