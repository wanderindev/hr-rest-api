from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

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

        sch = ScheduleModel.find_by_id(schedule_id,
                                       current_identity.organization_id)
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

        sch = ScheduleModel(data['start_date'],
                            data['department_id'])

        try:
            sch.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred while creating '
                               'the schedule.'}, 500

        return {
                   'message': 'Schedule created successfully.',
                   'schedule': ScheduleModel.find_by_id(
                       sch.id, current_identity.organization_id
                   ).to_dict()
               }, 201

    @jwt_required()
    def put(self,  schedule_id):
        data = Schedule.parser.parse_args()

        sch = ScheduleModel.find_by_id(schedule_id,
                                       current_identity.organization_id)

        if sch:
            sch.start_date = data['start_date']

            try:
                sch.save_to_db()
                return {
                   'message': 'Schedule updated successfully.',
                   'schedule': ScheduleModel.find_by_id(
                       sch.id, current_identity.organization_id
                   ).to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the schedule.'}, 500

        return {'message': 'Schedule not found.'}, 404

    @jwt_required()
    def delete(self, schedule_id):
        sch = ScheduleModel.find_by_id(schedule_id,
                                       current_identity.organization_id)

        if sch:
            try:
                sch.inactivate()
                return {'message': 'Schedule deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting'
                                   'the schedule.'}, 500

        return {'message': 'Schedule not found.'}, 404
