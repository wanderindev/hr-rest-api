from db import db
from models.enum import GENDER, PAYMENT_METHOD, TERMINATION_REASON, \
    TYPE_OF_CONTRACT
from models.emergency_contact import EmergencyContactModel
from models.health_permit import HealthPermitModel
from models.mixin import ModelMixin
from models.passport import PassportModel


class EmployeeModel(ModelMixin, db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    second_name = db.Column(db.String(40))
    first_surname = db.Column(db.String(40), nullable=False)
    second_surname = db.Column(db.String(40))
    national_id_number = db.Column(db.String(20))
    is_panamanian = db.Column(db.Boolean, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(GENDER, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    home_phone = db.Column(db.String(10))
    mobile_phone = db.Column(db.String(10))
    email = db.Column(db.String(50))
    type_of_contract = db.Column(TYPE_OF_CONTRACT, nullable=False)
    employment_date = db.Column(db.Date, nullable=False)
    contract_expiration_date = db.Column(db.Date)
    termination_date = db.Column(db.Date)
    termination_reason = db.Column(TERMINATION_REASON)
    salary_per_payment_period = db.Column(db.Numeric(7, 2), nullable=False)
    representation_expenses_per_payment_period = db.Column(db.Numeric(7, 2),
                                                           nullable=False)
    payment_method = db.Column(PAYMENT_METHOD, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, index=True)
    marital_status_id = db.Column(db.Integer,
                                  db.ForeignKey('marital_status.id'),
                                  nullable=False)
    department_id = db.Column(db.Integer,
                              db.ForeignKey('department.id'), nullable=False,
                              index=True)
    position_id = db.Column(db.Integer,
                            db.ForeignKey('employment_position.id'),
                            nullable=False, index=True)
    shift_id = db.Column(db.Integer,
                         db.ForeignKey('shift.id'), nullable=False)

    emergency_contacts = db.relationship(EmergencyContactModel,
                                         backref='employee',
                                         lazy='joined')
    health_permits = db.relationship(HealthPermitModel,
                                     backref='employee',
                                     lazy='joined')
    passports = db.relationship(PassportModel,
                                backref='employee',
                                lazy='joined')

    def __init__(self, first_name, second_name, first_surname, second_surname,
                 national_id_number, is_panamanian, date_of_birth, gender,
                 address, home_phone, mobile_phone, email, type_of_contract,
                 employment_date, contract_expiration_date, termination_date,
                 termination_reason, salary_per_payment_period,
                 representation_expenses_per_payment_period, payment_method,
                 is_active, marital_status_id, department_id, position_id,
                 shift_id):
        self.first_name = first_name
        self.second_name = second_name
        self.first_surname = first_surname
        self.second_surname = second_surname
        self. national_id_number = national_id_number
        self.is_panamanian = is_panamanian
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.address = address
        self.home_phone = home_phone
        self.mobile_phone = mobile_phone
        self.email = email
        self.type_of_contract = type_of_contract
        self.employment_date = employment_date
        self.contract_expiration_date = contract_expiration_date
        self.termination_date = termination_date
        self.termination_reason = termination_reason
        self.salary_per_payment_period = salary_per_payment_period
        self.representation_expenses_per_payment_period = \
            representation_expenses_per_payment_period
        self.payment_method = payment_method
        self.is_active = is_active
        self.marital_status_id = marital_status_id
        self.department_id = department_id
        self.position_id = position_id
        self.shift_id = shift_id

    @classmethod
    def find_by_id(cls, _id, organization_id):
        from models.department import DepartmentModel

        empl = cls.query.filter_by(id=_id).first()

        if empl:
            if DepartmentModel.find_by_id(
                    empl.department_id,
                    organization_id).organization_id == organization_id:
                return empl

    @classmethod
    def find_by_name(cls, first_name, second_name, first_surname,
                     second_surname, organization_id):
        from models.department import DepartmentModel

        empl = cls.query.filter_by(first_name=first_name,
                                   second_name=second_name,
                                   first_surname=first_surname,
                                   second_surname=second_surname,
                                   is_active=True).first()

        if empl:
            if DepartmentModel.find_by_id(
                    empl.department_id,
                    organization_id).organization_id == organization_id:
                return empl
