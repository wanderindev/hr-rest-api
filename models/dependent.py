from db import db
from models.enum import GENDER
from models.mixin import ModelMixin


class DependentModel(ModelMixin, db.Model):
    __tablename__ = 'dependent'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    second_name = db.Column(db.String(40), nullable=False)
    first_surname = db.Column(db.String(40), nullable=False)
    second_surname = db.Column(db.String(40), nullable=False)
    gender = db.Column(GENDER, nullable=False)
    date_of_birth = db.Column(db.Date)
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)
    family_relation_id = db.Column(db.Integer,
                                   db.ForeignKey('family_relation.id'),
                                   nullable=False, index=True)

    def __init__(self, first_name, second_name, first_surname, second_surname,
                 gender, date_of_birth, employee_id, family_relation_id):
        self.first_name = first_name
        self.second_name = second_name
        self.first_surname = first_surname
        self.second_surname = second_surname
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.employee_id = employee_id
        self.family_relation_id = family_relation_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.employee import EmployeeModel

        depen = cls.query.filter_by(id=_id).first()

        if depen:
            if EmployeeModel.find_by_id(depen.employee_id, user):
                return depen
