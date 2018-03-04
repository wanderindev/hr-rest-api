from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.employee import EmployeeModel
from models.passport import PassportModel


class Passport(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('passport_number',
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
    parser.add_argument('country_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, passport_id):
        passp = PassportModel.find_by_id(passport_id, current_identity)

        if passp:
            return passp.to_dict()

        return {'message': 'Passport not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Passport.parser.parse_args()

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            passp = PassportModel(data['passport_number'],
                                  data['issue_date'],
                                  data['expiration_date'],
                                  data['employee_id'],
                                  data['country_id'])

            try:
                passp.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the passport.'}, 500

            return {
                       'message': 'Passport created successfully.',
                       'passport': PassportModel.find_by_id(
                           passp.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create a passport '
                           'for an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  passport_id):
        data = Passport.parser.parse_args()

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            passp = PassportModel.find_by_id(passport_id, current_identity)

            if passp:
                passp.passport_number = data['passport_number']
                passp.issue_date = data['issue_date']
                passp.expiration_date = data['expiration_date']
                passp.employee_id = data['employee_id']
                passp.country_id = data['country_id']

                try:
                    passp.save_to_db()
                    return {
                       'message': 'Passport updated successfully.',
                       'passport': PassportModel.find_by_id(
                           passp.id, current_identity
                       ).to_dict()
                    }, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while updating '
                                       'the passport.'}, 500

            return {'message': 'Passport not found.'}, 404

        return {'message': 'You are not allowed to assign an passport '
                           'to an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def delete(self, passport_id):
        passp = PassportModel.find_by_id(passport_id, current_identity)

        if passp:
            try:
                passp.delete_from_db()
                return {'message': 'Passport deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting'
                                   'the passport.'}, 500

        return {'message': 'Passport not found.'}, 404
