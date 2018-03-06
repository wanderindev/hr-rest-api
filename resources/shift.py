from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.shift import ShiftModel
from utils import get_time


class Shift(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('shift_name',
                        type=str,
                        required=True)
    parser.add_argument('weekly_hours',
                        type=float,
                        required=True)
    parser.add_argument('is_rotating',
                        type=bool,
                        required=True)
    parser.add_argument('payment_period',
                        type=str,
                        required=True)
    parser.add_argument('break_length',
                        type=str,
                        required=True)
    parser.add_argument('is_break_included_in_shift',
                        type=bool,
                        required=True)
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=False)
    parser.add_argument('organization_id',
                        type=int,
                        required=True)
    parser.add_argument('rotation_start_hour',
                        type=str,
                        required=False)
    parser.add_argument('rotation_end_hour',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_hour_monday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_break_hour_monday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_break_hour_monday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_hour_monday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_hour_tuesday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_break_hour_tuesday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_break_hour_tuesday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_hour_tuesday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_hour_wednesday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_break_hour_wednesday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_break_hour_wednesday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_hour_wednesday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_hour_thursday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_break_hour_thursday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_break_hour_thursday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_hour_thursday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_hour_friday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_break_hour_friday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_break_hour_friday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_hour_friday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_hour_saturday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_break_hour_saturday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_break_hour_saturday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_hour_saturday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_hour_sunday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_start_break_hour_sunday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_break_hour_sunday',
                        type=str,
                        required=False)
    parser.add_argument('fixed_end_hour_sunday',
                        type=str,
                        required=False)
    parser.add_argument('rest_day',
                        type=str,
                        required=False)

    @jwt_required()
    def get(self, shift_id):
        shift = ShiftModel.find_by_id(shift_id, current_identity)
        if shift:
            return shift.to_dict()

        return {'message': 'Shift not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Shift.parser.parse_args()

        if ShiftModel.query.filter_by(
                shift_name=data['shift_name'],
                organization_id=data['organization_id']).first():
            return {'message': 'A shift with that name already '
                               'exists in the organization.'}, 400

        if current_identity.organization_id == data['organization_id'] or \
                current_identity.is_super:
            shift = ShiftModel(**data)

            try:
                shift.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the shift.'}, 500

            return {
                       'message': 'Shift created successfully.',
                       'shift': ShiftModel.find_by_id(
                           shift.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create a shift '
                           'that does not belong to your organization.'}, 403

    @jwt_required()
    def put(self,  shift_id):
        data = Shift.parser.parse_args()

        shift = ShiftModel.find_by_id(shift_id, current_identity)

        if shift:
            shift.shift_name = data['shift_name']
            shift.weekly_hours = data['weekly_hours']
            shift.is_rotating = data['is_rotating']
            shift.payment_period = data['payment_period']
            shift.break_length = data['break_length']
            shift.is_break_included_in_shift = data[
                'is_break_included_in_shift']
            shift.rotation_start_hour = data.get('rotation_start_hour')
            shift.rotation_end_hour = data.get('rotation_end_hour')
            shift.fixed_start_hour_monday = data.get('fixed_start_hour_monday')
            shift.fixed_start_break_hour_monday = data.get(
                'fixed_start_break_hour_monday')
            shift.fixed_end_break_hour_monday = data.get(
                'fixed_end_break_hour_monday')
            shift.fixed_end_hour_monday = data.get('fixed_end_hour_monday')
            shift.fixed_start_hour_tuesday = data.get(
                'fixed_start_hour_tuesday')
            shift.fixed_start_break_hour_tuesday = data.get(
                'fixed_start_break_hour_tuesday')
            shift.fixed_end_break_hour_tuesday = data.get(
                'fixed_end_break_hour_tuesday')
            shift.fixed_end_hour_tuesday = data.get('fixed_end_hour_tuesday')
            shift.fixed_start_hour_wednesday = data.get(
                'fixed_start_hour_wednesday')
            shift.fixed_start_break_hour_wednesday = data.get(
                'fixed_start_break_hour_wednesday')
            shift.fixed_end_break_hour_wednesday = data.get(
                'fixed_end_break_hour_wednesday')
            shift.fixed_end_hour_wednesday = data.get(
                'fixed_end_hour_wednesday')
            shift.fixed_start_hour_thursday = data.get(
                'fixed_start_hour_thursday')
            shift.fixed_start_break_hour_thursday = data.get(
                'fixed_start_break_hour_thursday')
            shift.fixed_end_break_hour_thursday = data.get(
                'fixed_end_break_hour_thursday')
            shift.fixed_end_hour_thursday = data.get('fixed_end_hour_thursday')
            shift.fixed_start_hour_friday = data.get('fixed_start_hour_friday')
            shift.fixed_start_break_hour_friday = data.get(
                'fixed_start_break_hour_friday')
            shift.fixed_end_break_hour_friday = data.get(
                'fixed_end_break_hour_friday')
            shift.fixed_end_hour_friday = data.get('fixed_end_hour_friday')
            shift.fixed_start_hour_saturday = data.get(
                'fixed_start_hour_saturday')
            shift.fixed_start_break_hour_saturday = data.get(
                'fixed_start_break_hour_saturday')
            shift.fixed_end_break_hour_saturday = data.get(
                'fixed_end_break_hour_saturday')
            shift.fixed_end_hour_saturday = data.get('fixed_end_hour_saturday')
            shift.fixed_start_hour_sunday = data.get('fixed_start_hour_sunday')
            shift.fixed_start_break_hour_sunday = data.get(
                'fixed_start_break_hour_sunday')
            shift.fixed_end_break_hour_sunday = data.get(
                'fixed_end_break_hour_sunday')
            shift.fixed_end_hour_sunday = data.get('fixed_end_hour_sunday')
            shift.rest_day = data.get('rest_day')

            try:
                shift.save_to_db()
                return {
                           'message': 'Shift updated successfully.',
                           'shift': ShiftModel.find_by_id(
                               shift.id, current_identity
                           ).to_dict()
                       }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the shift.'}, 500

        return {'message': 'Shift not found.'}, 404

    @jwt_required()
    def delete(self, shift_id):
        shift = ShiftModel.find_by_id(shift_id, current_identity)

        if shift:
            if shift.is_active:
                try:
                    shift.inactivate()
                    return {'message': 'Shift is now inactive.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while inactivating'
                                       'the shift.'}, 500
            else:
                return {'message': 'Shift was already inactive.'}, 400

        return {'message': 'Shift not found.'}, 404


class ActivateShift(Resource):
    @jwt_required()
    def put(self, shift_id):
        shift = ShiftModel.find_by_id(shift_id, current_identity)

        if shift:
            if not shift.is_active:
                try:
                    shift.activate()
                    return {'message': 'Shift is now active.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while activating'
                                       'the shift.'}, 500
            else:
                return {'message': 'Shift was already active.'}, 400

        return {'message': 'Shift not found.'}, 404
