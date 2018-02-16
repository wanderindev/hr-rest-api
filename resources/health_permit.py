from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

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

        e_cont = HealthPermitModel.find_by_id(
            permit_id, current_identity.organization_id)
        if e_cont:
            return e_cont.to_dict()

        return {'message': 'Health permit not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = HealthPermit.parser.parse_args()

        e_cont = HealthPermitModel(data['health_permit_type'],
                                   data['issue_date'],
                                   data['expiration_date'],
                                   data['employee_id'])

        try:
            e_cont.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred creating '
                               'the health permit.'}, 500

        return {
                   'message': 'Health permit created successfully.',
                   'health_permit': HealthPermitModel.find_by_id(
                       e_cont.id, current_identity.organization_id
                   ).to_dict()
               }, 201

    @jwt_required()
    def put(self,  permit_id):
        data = HealthPermit.parser.parse_args()

        e_cont = HealthPermitModel.find_by_id(
            permit_id, current_identity.organization_id)

        if e_cont:
            e_cont.health_permit_type = data['health_permit_type']
            e_cont.issue_date = data['issue_date']
            e_cont.expiration_date = data['expiration_date']
            e_cont.employee_id = data['employee_id']

            try:
                e_cont.save_to_db()
                return {
                   'message': 'Health permit updated successfully.',
                   'health_permit': HealthPermitModel.find_by_id(
                       e_cont.id, current_identity.organization_id
                   ).to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred updating '
                                   'the health permit.'}, 500

        return {'message': 'Health permit not found.'}, 404

    @jwt_required()
    def delete(self, permit_id):
        e_cont = HealthPermitModel.find_by_id(
            permit_id, current_identity.organization_id)

        if e_cont:
            try:
                e_cont.delete_from_db()
                return {'message': 'Health permit deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting'
                                   'the health permit.'}, 500

        return {'message': 'Health permit not found.'}, 404
