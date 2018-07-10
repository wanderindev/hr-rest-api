from db import db

from models.mixin import ModelMixin


class UniformRequirementModel(ModelMixin, db.Model):
    __tablename__ = 'uniform_requirement'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('employee.id'),
                            nullable=False, index=True)
    uniform_item_id = db.Column(db.Integer,
                                db.ForeignKey('uniform_item.id'),
                                nullable=False, index=True)
    uniform_size_id = db.Column(db.Integer,
                                db.ForeignKey('uniform_size.id'),
                                nullable=False, index=True)

    def __init__(self, employee_id, uniform_item_id, uniform_size_id):
        self.employee_id = employee_id
        self.uniform_item_id = uniform_item_id
        self.uniform_size_id = uniform_size_id

    @classmethod
    def find_by_id(cls, _id, user):
        from models.employee import EmployeeModel
        from models.uniform_item import UniformItemModel

        record = cls.query.filter_by(id=_id).first()

        if record:
            if UniformItemModel.find_by_id(record.uniform_item_id, user) and \
                    EmployeeModel.find_by_id(record.employee_id, user):
                return record

    @classmethod
    def find_all(cls, user, employee_id):
        from models.employee import EmployeeModel

        records = cls.query.filter_by(employee_id=employee_id).all()

        if records and EmployeeModel.find_by_id(employee_id, user):
            return records
