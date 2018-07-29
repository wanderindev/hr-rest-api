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
    def find_all(cls, user, employee_id):
        from models.employee import EmployeeModel

        records = cls.query.filter_by(userid=employee_id).all()

        if records and EmployeeModel.find_by_id(employee_id, user):
            return records
