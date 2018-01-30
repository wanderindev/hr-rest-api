from db import db
from models.mixin import ModelsMixin


class MaritalStatusModel(ModelsMixin, db.Model):
    __tablename__ = 'marital_status'

    id = db.Column(db.Integer, primary_key=True)
    status_feminine = db.Column(db.String(25), nullable=False)
    status_masculine = db.Column(db.String(25), nullable=False)

    def __init__(self, status_feminine, status_masculine):
        self.status_feminine = status_feminine
        self.status_masculine = status_masculine
