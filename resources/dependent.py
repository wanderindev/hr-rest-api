from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.dependent import DependentModel
from models.employee import EmployeeModel


class Dependent(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        required=True)
    parser.add_argument('second_name',
                        type=str,
                        required=True)
    parser.add_argument('first_surname',
                        type=str,
                        required=True)
    parser.add_argument('second_surname',
                        type=str,
                        required=True)
    parser.add_argument('gender',
                        type=str,
                        required=True)
    parser.add_argument('date_of_birth',
                        type=str,
                        required=False)
    parser.add_argument('employee_id',
                        type=int,
                        required=True)
    parser.add_argument('family_relation_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, dependent_id):

        depen = DependentModel.find_by_id(dependent_id, current_identity)
        if depen:
            return depen.to_dict()

        return {'message': 'Dependent not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Dependent.parser.parse_args()

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            depen = DependentModel(data['first_name'],
                                   data['second_name'],
                                   data['first_surname'],
                                   data['second_surname'],
                                   data['gender'],
                                   data['date_of_birth'],
                                   data['employee_id'],
                                   data['family_relation_id'])

            try:
                depen.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the dependent.'}, 500

            return {
                       'message': 'Dependent created successfully.',
                       'dependent': DependentModel.find_by_id(
                           depen.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create an dependent '
                           'for an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  dependent_id):
        data = Dependent.parser.parse_args()

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            depen = DependentModel.find_by_id(dependent_id, current_identity)

            if depen:
                depen.first_name = data['first_name']
                depen.second_name = data['second_name']
                depen.first_surname = data['first_surname']
                depen.second_surname = data['second_surname']
                depen.gender = data['gender']
                depen.date_of_birth = data['date_of_birth']
                depen.employee_id = data['employee_id']
                depen.family_relation_id = data['family_relation_id']

                try:
                    depen.save_to_db()
                    return {
                       'message': 'Dependent updated successfully.',
                       'dependent': DependentModel.find_by_id(
                           depen.id, current_identity
                       ).to_dict()
                    }, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while updating '
                                       'the dependent.'}, 500

            return {'message': 'Dependent not found.'}, 404

        return {'message': 'You are not allowed to assign an dependent '
                           'to an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def delete(self, dependent_id):
        depen = DependentModel.find_by_id(dependent_id, current_identity)

        if depen:
            try:
                depen.delete_from_db()
                return {'message': 'Dependent deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting'
                                   'the dependent.'}, 500

        return {'message': 'Dependent not found.'}, 404
