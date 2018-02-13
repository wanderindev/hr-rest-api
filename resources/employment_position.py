from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.employment_position import EmploymentPositionModel


class EmploymentPosition(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('position_name_feminine',
                        type=str,
                        required=True)
    parser.add_argument('position_name_masculine',
                        type=str,
                        required=True)
    parser.add_argument('minimum_hourly_wage',
                        type=float,
                        required=False)
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=False)
    parser.add_argument('organization_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, position_name):
        e_p = EmploymentPositionModel.find_by_name(
            position_name, current_identity.organization_id)
        if e_p:
            return e_p.to_dict()

        return {'message': 'Employment position not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = EmploymentPosition.parser.parse_args()

        if EmploymentPositionModel.find_by_name(
                data['position_name_feminine'],
                data['organization_id']) or \
           EmploymentPositionModel.find_by_name(
               data['position_name_masculine'],
               data['organization_id']):
            return {'message': 'An employment position with that name already '
                               'exists in the organization.'}, 400

        e_p = EmploymentPositionModel(data['position_name_feminine'],
                                      data['position_name_masculine'],
                                      data['minimum_hourly_wage'],
                                      data['is_active'],
                                      data['organization_id'])

        try:
            e_p.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred creating '
                               'the employment position.'}, 500

        return {
                   'message': 'Employment position created successfully.',
                   'employment_position': EmploymentPositionModel
                   .find_by_id(
                       e_p.id,
                       current_identity.organization_id).to_dict()
               }, 201

    @jwt_required()
    def put(self,  position_name):
        data = EmploymentPosition.parser.parse_args()

        e_p = EmploymentPositionModel.find_by_name(
            position_name, current_identity.organization_id)

        if e_p:
            e_p.position_name_feminine = data['position_name_feminine']
            e_p.position_name_masculine = data['position_name_masculine']
            e_p.minimum_hourly_wage = data['minimum_hourly_wage']

            try:
                e_p.save_to_db()
                return {
                           'message': 'Employment position updated '
                                      'successfully.',
                           'employment_position': EmploymentPositionModel
                           .find_by_id(
                               e_p.id,
                               current_identity.organization_id).to_dict()
                       }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred updating '
                                   'the employment position.'}, 500

        return {'message': 'Employment position not found.'}, 404

    @jwt_required()
    def delete(self, position_name):
        e_p = EmploymentPositionModel.find_by_name(
            position_name, current_identity.organization_id)

        if e_p:
            if e_p.is_active:
                try:
                    e_p.inactivate()
                    return {'message': 'Employment position is '
                                       'now inactive.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while inactivating'
                                       'the employment position.'}, 500
            else:
                return {'message': 'Employment position was '
                                   'already inactive.'}, 400

        return {'message': 'Employment position not found.'}, 404


class ActivateEmploymentPosition(Resource):
    @jwt_required()
    def put(self, position_name):
        e_p = EmploymentPositionModel.find_by_name(
            position_name, current_identity.organization_id)

        if e_p:
            if not e_p.is_active:
                try:
                    e_p.activate()
                    return {'message': 'Employment position is '
                                       'now active.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while activating'
                                       'the employment position.'}, 500
            else:
                return {'message': 'Employment position was '
                                   'already active.'}, 400

        return {'message': 'Employment position not found.'}, 404
