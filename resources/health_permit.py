from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.employee import EmployeeModel
from models.health_permit import HealthPermitModel


class HealthPermit(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('health_permit_type',
                        type=str,
                        required=True)
    parser.add_argument('issue_date',
                        type=str,
                        required=True)
    parser.add_argument('expiration_date',
                        type=str,
                        required=True)
    parser.add_argument('employee_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, permit_id):
        h_p = HealthPermitModel.find_by_id(permit_id, current_identity)

        if h_p:
            return h_p.to_dict()

        return {'message': 'Health permit not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = HealthPermit.parser.parse_args()

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            h_p = HealthPermitModel(**data)

            try:
                h_p.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the health permit.'}, 500

            return {
                       'message': 'Health permit created successfully.',
                       'health_permit': HealthPermitModel.find_by_id(
                           h_p.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create a health permit '
                           'for an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  permit_id):
        data = HealthPermit.parser.parse_args()

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            h_p = HealthPermitModel.find_by_id(permit_id, current_identity)

            if h_p:
                h_p.health_permit_type = data['health_permit_type']
                h_p.issue_date = data['issue_date']
                h_p.expiration_date = data['expiration_date']
                h_p.employee_id = data['employee_id']

                try:
                    h_p.save_to_db()
                    return {
                       'message': 'Health permit updated successfully.',
                       'health_permit': HealthPermitModel.find_by_id(
                           h_p.id, current_identity
                       ).to_dict()
                    }, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while updating '
                                       'the health permit.'}, 500

            return {'message': 'Health permit not found.'}, 404

        return {'message': 'You are not allowed to assign a health permit '
                           'to an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def delete(self, permit_id):
        h_p = HealthPermitModel.find_by_id(permit_id, current_identity)

        if h_p:
            try:
                h_p.delete_from_db()
                return {'message': 'Health permit deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting'
                                   'the health permit.'}, 500

        return {'message': 'Health permit not found.'}, 404
