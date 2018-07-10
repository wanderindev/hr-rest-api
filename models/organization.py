from sqlalchemy import UniqueConstraint

from db import db
from models.creditor import CreditorModel
from models.department import DepartmentModel
from models.employment_position import EmploymentPositionModel
from models.mixin import ModelMixin
from models.shift import ShiftModel
from models.uniform_item import UniformItemModel
from models.user import AppUserModel


class OrganizationModel(ModelMixin, db.Model):
    __tablename__ = 'organization'
    __table_args__ = (UniqueConstraint('organization_name',
                                       name='organization_'
                                            'organization_name_uindex'),)

    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    app_users = db.relationship(AppUserModel,
                                backref='organization',
                                lazy='joined')

    employment_positions = db.relationship(EmploymentPositionModel,
                                           backref='organization',
                                           lazy='joined')

    departments = db.relationship(DepartmentModel,
                                  backref='organization',
                                  lazy='joined')

    shifts = db.relationship(ShiftModel,
                             backref='organization',
                             lazy='joined')

    uniform_items = db.relationship(UniformItemModel,
                                    backref='organization',
                                    lazy='joined')

    creditors = db.relationship(CreditorModel,
                                backref='organization',
                                lazy='joined')

    def __init__(self, organization_name, is_active):
        self.organization_name = organization_name
        self.is_active = is_active

    @classmethod
    def find_by_id(cls, _id, user):
        if user.is_super or user.organization_id == _id:
            return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls, user):
        if user.is_super:
            return cls.query.all()