from db import db
from models.enum import ATT_TYPE
from models.mixin import ModelMixin


class RawAttendanceModel(ModelMixin, db.Model):
    __tablename__ = 'raw_attendance'

    exclude_from_update = ('stgid', 'userid', 'att_time', 'att_type')

    id = db.Column(db.Integer, primary_key=True)
    stgid = db.Column(db.String(20), nullable=False)
    userid = db.Column(db.Integer, nullable=False)
    att_time = db.Column(db.BigInteger, nullable=False)
    att_type = db.Column(ATT_TYPE, nullable=False)
    was_processed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, stgid, userid, att_time, att_type):
        self.stgid = stgid
        self.userid = userid
        self.att_time = att_time
        self.att_type = att_type

    @classmethod
    def find_by_id(cls, _id, user):
        from models.employee import EmployeeModel

        record = cls.query.filter_by(id=_id).first()

        if record:
            if EmployeeModel.find_by_id(record.userid, user):
                return record

    @classmethod
    def find_all(cls, user):
        from models.department import DepartmentModel
        from models.employee import EmployeeModel

        departments = DepartmentModel.find_all(user)
        d_ids = [department.id for department in departments]

        employees = EmployeeModel.query.filter(
            EmployeeModel.department_id.in_(d_ids)).all()
        e_ids = [employee.id for employee in employees]

        return cls.query.filter(cls.userid.in_(e_ids),
                                cls.was_processed==False).all()
