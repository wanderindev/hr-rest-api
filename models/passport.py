from db import db
from models.mixin import ModelMixin


class PassportModel(ModelMixin, db.Model):
    __tablename__ = 'passport'

    id = db.Column(db.Integer, primary_key=True)
    passport_number = db.Column(db.String(40), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)
    country_id = db.Column(db.Integer,
                           db.ForeignKey('country.id'),
                           nullable=False, index=True)

    def __init__(self, passport_number, issue_date, expiration_date,
                 employee_id, country_id):
        self.passport_number = passport_number
        self.issue_date = issue_date
        self.expiration_date = expiration_date
        self.employee_id = employee_id
        self.country_id = country_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.employee import EmployeeModel

        passport = cls.query.filter_by(id=_id).first()

        if passport:
            if EmployeeModel.find_by_id(passport.employee_id, user):
                return passport

    @classmethod
    def find_all(cls, user, employee_id):
        from models.employee import EmployeeModel

        records = cls.query.filter_by(employee_id=employee_id).all()

        if records and EmployeeModel.find_by_id(employee_id, user):
            return records
