from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.employee import EmployeeModel
from models.schedule_detail import ScheduleDetailModel


class ScheduleDetail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('day_1_start',
                        type=str,
                        required=False)
    parser.add_argument('day_1_end',
                        type=str,
                        required=False)
    parser.add_argument('day_1_comment',
                        type=str,
                        required=False)
    parser.add_argument('day_2_start',
                        type=str,
                        required=False)
    parser.add_argument('day_2_end',
                        type=str,
                        required=False)
    parser.add_argument('day_2_comment',
                        type=str,
                        required=False)
    parser.add_argument('day_3_start',
                        type=str,
                        required=False)
    parser.add_argument('day_3_end',
                        type=str,
                        required=False)
    parser.add_argument('day_3_comment',
                        type=str,
                        required=False)
    parser.add_argument('day_4_start',
                        type=str,
                        required=False)
    parser.add_argument('day_4_end',
                        type=str,
                        required=False)
    parser.add_argument('day_4_comment',
                        type=str,
                        required=False)
    parser.add_argument('day_5_start',
                        type=str,
                        required=False)
    parser.add_argument('day_5_end',
                        type=str,
                        required=False)
    parser.add_argument('day_5_comment',
                        type=str,
                        required=False)
    parser.add_argument('day_6_start',
                        type=str,
                        required=False)
    parser.add_argument('day_6_end',
                        type=str,
                        required=False)
    parser.add_argument('day_6_comment',
                        type=str,
                        required=False)
    parser.add_argument('day_7_start',
                        type=str,
                        required=False)
    parser.add_argument('day_7_end',
                        type=str,
                        required=False)
    parser.add_argument('day_7_comment',
                        type=str,
                        required=False)
    parser.add_argument('employee_id',
                        type=int,
                        required=True)
    parser.add_argument('schedule_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, detail_id):
        sch_d = ScheduleDetailModel.find_by_id(detail_id, current_identity)

        if sch_d:
            return sch_d.to_dict()

        return {'message': 'Schedule detail not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = ScheduleDetail.parser.parse_args()

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            sch_d = ScheduleDetailModel(**data)

            try:
                sch_d.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the schedule detail.'}, 500

            return {
                       'message': 'Schedule detail created successfully.',
                       'schedule_detail': ScheduleDetailModel.find_by_id(
                           sch_d.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create an schedule detail '
                           'for an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  detail_id):
        data = ScheduleDetail.parser.parse_args()

        sch_d = ScheduleDetailModel.find_by_id(detail_id, current_identity)

        if sch_d:
            try:
                _, sch_d = sch_d.update(data, ('schedule_id', 'employee_id'))
                return {
                   'message': 'Schedule detail updated successfully.',
                   'schedule_detail': sch_d.to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the schedule detail.'}, 500

        return {'message': 'Schedule detail not found.'}, 404

    @jwt_required()
    def delete(self, detail_id):
        sch_d = ScheduleDetailModel.find_by_id(detail_id, current_identity)

        if sch_d:
            try:
                sch_d.delete_from_db()
                return {'message': 'Schedule detail deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting'
                                   'the schedule detail.'}, 500

        return {'message': 'Schedule detail not found.'}, 404
