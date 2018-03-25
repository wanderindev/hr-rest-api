from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.payment import PaymentModel
from models.employee import EmployeeModel


class Payment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('payment_date',
                        type=str,
                        required=True)
    parser.add_argument('document_number',
                        type=str,
                        required=True)
    parser.add_argument('employee_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, payment_id):
        pmt = PaymentModel.find_by_id(payment_id, current_identity)

        if pmt:
            return pmt.to_dict()

        return {'message': 'Payment not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Payment.parser.parse_args()

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            pmt = PaymentModel(**data)

            try:
                pmt.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the payment.'}, 500

            return {
                       'message': 'Payment created successfully.',
                       'payment': PaymentModel.find_by_id(
                           pmt.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create an payment '
                           'for an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  payment_id):
        data = Payment.parser.parse_args()

        pmt = PaymentModel.find_by_id(payment_id, current_identity)

        if pmt:
            try:
                _, pmt = pmt.update(data, ('employee_id',))
                return {
                   'message': 'Payment updated successfully.',
                   'payment': pmt.to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the payment.'}, 500

        return {'message': 'Payment not found.'}, 404

    @jwt_required()
    def delete(self, payment_id):
        pmt = PaymentModel.find_by_id(payment_id, current_identity)

        if pmt:
            try:
                pmt.delete_from_db()
                return {'message': 'Payment deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting'
                                   'the payment.'}, 500

        return {'message': 'Payment not found.'}, 404
