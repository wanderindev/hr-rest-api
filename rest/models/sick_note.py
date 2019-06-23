from db import db
from models.mixin import ModelMixin


class SickNoteModel(ModelMixin, db.Model):
    __tablename__ = 'sick_note'
    exclude_from_update = ('employee_id',)

    id = db.Column(db.Integer, primary_key=True)
    sick_note_date = db.Column(db.Date, nullable=False)
    number_of_hours_requested = db.Column(db.Numeric(5, 2), nullable=False)
    number_of_hours_approved = db.Column(db.Numeric(5, 2), nullable=False)
    date_received = db.Column(db.Date, nullable=False)
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)

    def __init__(self, sick_note_date, number_of_hours_requested,
                 number_of_hours_approved, date_received, employee_id):
        self.sick_note_date = sick_note_date
        self.number_of_hours_requested = number_of_hours_requested
        self.number_of_hours_approved = number_of_hours_approved
        self.date_received = date_received
        self.employee_id = employee_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.employee import EmployeeModel

        record = cls.query.filter_by(id=_id).first()

        if record:
            if EmployeeModel.find_by_id(record.employee_id, user):
                return record

    @classmethod
    def find_all(cls, user, employee_id):
        from models.employee import EmployeeModel

        records = cls.query.filter_by(employee_id=employee_id).all()

        if records and EmployeeModel.find_by_id(employee_id, user):
            return records
