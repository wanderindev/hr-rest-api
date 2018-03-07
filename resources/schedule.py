from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.department import DepartmentModel
from models.schedule import ScheduleModel


class Schedule(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('start_date',
                        type=str,
                        required=True)
    parser.add_argument('department_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, schedule_id):
        sch = ScheduleModel.find_by_id(schedule_id, current_identity)
        if sch:
            return sch.to_dict()

        return {'message': 'Schedule not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Schedule.parser.parse_args()

        if ScheduleModel.query.filter_by(
                start_date=data['start_date'],
                department_id=data['department_id']).first():
            return {'message': 'A schedule for that department and date '
                               'already exists in the table.'}, 400

        if DepartmentModel.find_by_id(data['department_id'], current_identity):
            sch = ScheduleModel(**data)

            try:
                sch.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the schedule.'}, 500

            return {
                       'message': 'Schedule created successfully.',
                       'schedule': ScheduleModel.find_by_id(
                           sch.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to add a schedule to a '
                           'department that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  schedule_id):
        data = Schedule.parser.parse_args()

        if ScheduleModel.query.filter_by(**data).first():
            return {'message': 'A schedule for that department and date '
                               'already exists in the table.'}, 400

        if DepartmentModel.find_by_id(data['department_id'], current_identity):
            sch = ScheduleModel.find_by_id(schedule_id, current_identity)

            if sch:
                try:
                    _, sch = sch.update(data)
                    return {
                       'message': 'Schedule updated successfully.',
                       'schedule': sch.to_dict()
                    }, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while updating '
                                       'the schedule.'}, 500

            return {'message': 'Schedule not found.'}, 404

        return {'message': 'You are not allowed to move a schedule to a '
                           'department that does not belong to your'
                           'organization.'}, 403

    @jwt_required()
    def delete(self, schedule_id):
        sch = ScheduleModel.find_by_id(schedule_id, current_identity)

        if sch:
            try:
                sch.delete_from_db()
                return {'message': 'Schedule deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting'
                                   'the schedule.'}, 500

        return {'message': 'Schedule not found.'}, 404
