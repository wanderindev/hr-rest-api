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
    def get(self, position_id):
        e_p = EmploymentPositionModel.find_by_id(position_id, current_identity)
        if e_p:
            return e_p.to_dict()

        return {'message': 'Employment position not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = EmploymentPosition.parser.parse_args()

        if EmploymentPositionModel.query.filter_by(
                position_name_feminine=data['position_name_feminine'],
                organization_id=data['organization_id']).first() or \
                EmploymentPositionModel.query.filter_by(
                    position_name_masculine=data['position_name_masculine'],
                    organization_id=data['organization_id']).first():
            return {'message': 'An employment position with that name already '
                               'exists in the organization.'}, 400

        if current_identity.organization_id == data['organization_id'] or \
                current_identity.is_super:
            e_p = EmploymentPositionModel(**data)

            try:
                e_p.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the employment position.'}, 500

            return {
                       'message': 'Employment position created successfully.',
                       'employment_position': EmploymentPositionModel
                       .find_by_id(
                           e_p.id,
                           current_identity).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create an employment '
                           'position that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  position_id):
        data = EmploymentPosition.parser.parse_args()

        e_p = EmploymentPositionModel.find_by_id(position_id, current_identity)

        if e_p:
            try:
                _, e_p = e_p.update(data, ['is_active', 'organization_id'])
                return {
                   'message': 'Employment position updated '
                              'successfully.',
                   'employment_position': e_p.to_dict()
               }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the employment position.'}, 500

        return {'message': 'Employment position not found.'}, 404

    @jwt_required()
    def delete(self, position_id):
        e_p = EmploymentPositionModel.find_by_id(position_id, current_identity)

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
    def put(self, position_id):
        e_p = EmploymentPositionModel.find_by_id(position_id, current_identity)

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
