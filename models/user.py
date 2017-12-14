from db import db
from models.mixin import ModelsMixin


class UserModel(ModelsMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_super = db.Column(db.Boolean, default=False)
    is_owner = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    organization_id = db.Column(db.Integer,
                                db.ForeignKey('organizations.id'),
                                nullable=False)

    def __init__(self, username, password, organization_id,
                 is_super=False, is_owner=False, is_active=True):
        self.username = username
        self.password = password
        self.organization_id = organization_id
        self.is_super = is_super
        self.is_owner = is_owner
        self.is_active = is_active

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
