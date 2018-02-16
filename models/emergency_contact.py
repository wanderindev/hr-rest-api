from db import db
from models.mixin import ModelMixin


class EmergencyContactModel(ModelMixin, db.Model):
    __tablename__ = 'emergency_contact'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    home_phone = db.Column(db.String(10))
    work_phone = db.Column(db.String(10))
    mobile_phone = db.Column(db.String(10))
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)

    def __init__(self, first_name, last_name, home_phone, work_phone,
                 mobile_phone, employee_id):
        self.first_name = first_name
        self.last_name = last_name
        self.home_phone = home_phone
        self.work_phone = work_phone
        self.mobile_phone = mobile_phone
        self.employee_id = employee_id

    @classmethod
    def find_by_id(cls, _id, organization_id):
        from models.employee import EmployeeModel

        e_cont = cls.query.filter_by(id=_id).first()

        if e_cont:
            if EmployeeModel.find_by_id(e_cont.employee_id, organization_id):
                return e_cont
