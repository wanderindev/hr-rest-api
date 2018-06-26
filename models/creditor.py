from db import db
from models.mixin import ModelMixin


class CreditorModel(ModelMixin, db.Model):
    __tablename__ = 'creditor'

    id = db.Column(db.Integer, primary_key=True)
    creditor_name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, nullable=False)
    organization_id = db.Column(db.Integer,
                                db.ForeignKey('organization.id'),
                                nullable=False, index=True)

    def __init__(self, creditor_name, phone_number,
                 email, organization_id, is_active):
        self.creditor_name = creditor_name
        self.phone_number = phone_number
        self.email = email
        self.organization_id = organization_id
        self.is_active = is_active

    @classmethod
    def find_by_id(cls, _id, user):
        from models.organization import OrganizationModel

        cred = cls.query.filter_by(id=_id).first()

        if cred:
            if OrganizationModel.find_by_id(cred.organization_id, user):
                return cred
