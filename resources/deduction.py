from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.deduction import DeductionModel
from models.employee import EmployeeModel


class Deduction(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('start_date',
                        type=str,
                        required=True)
    parser.add_argument('end_date',
                        type=str,
                        required=True)
    parser.add_argument('deduction_per_payment_period',
                        type=float,
                        required=True)
    parser.add_argument('payment_method',
                        type=str,
                        required=True)
    parser.add_argument('deduct_in_december',
                        default=True,
                        type=bool,
                        required=True)
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=True)
    parser.add_argument('employee_id',
                        type=int,
                        required=True)
    parser.add_argument('creditor_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, deduction_id):
        ded = DeductionModel.find_by_id(deduction_id, current_identity)

        if ded:
            return ded.to_dict()

        return {'message': 'Deduction not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Deduction.parser.parse_args()

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            ded = DeductionModel(**data)

            try:
                ded.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the deduction.'}, 500

            return {
                       'message': 'Deduction created successfully.',
                       'deduction': DeductionModel.find_by_id(
                           ded.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create a deduction '
                           'for an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  deduction_id):
        data = Deduction.parser.parse_args()

        ded = DeductionModel.find_by_id(deduction_id, current_identity)

        if ded:
            try:
                _, ded = ded.update(data, ('is_active', 'employee_id', 'creditor_id'))
                return {
                   'message': 'Deduction updated successfully.',
                   'deduction': ded.to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the deduction.'}, 500

        return {'message': 'Deduction not found.'}, 404

    @jwt_required()
    def delete(self, deduction_id):
        ded = DeductionModel.find_by_id(deduction_id, current_identity)

        if ded:
            if ded.is_active:
                try:
                    ded.inactivate()
                    return {'message': 'Deduction is now inactive.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while inactivating'
                                       'the deduction.'}, 500
            else:
                return {'message': 'Deduction was already inactive.'}, 400

        return {'message': 'Deduction not found.'}, 404


class ActivateDeduction(Resource):
    @jwt_required()
    def put(self, deduction_id):
        ded = DeductionModel.find_by_id(deduction_id, current_identity)

        if ded:
            if not ded.is_active:
                try:
                    ded.activate()
                    return {'message': 'Deduction is now active.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while activating'
                                       'the deduction.'}, 500
            else:
                return {'message': 'Deduction was already active.'}, 400

        return {'message': 'Deduction not found.'}, 404
