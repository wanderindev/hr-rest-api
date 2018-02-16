from db import db
from models.mixin import ModelMixin


class CountryModel(ModelMixin, db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(80), nullable=False)
    nationality = db.Column(db.String(80), nullable=False)

    def __init__(self, country_name, nationality):
        self.country_name = country_name
        self.nationality = nationality

    @classmethod
    def find_all(cls):
        return cls.query.order_by('country_name').all()
