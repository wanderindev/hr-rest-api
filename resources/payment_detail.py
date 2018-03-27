from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.payment import PaymentModel
from models.payment_detail import PaymentDetailModel


class PaymentDetail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('payment_type',
                        type=str,
                        required=True)
    parser.add_argument('gross_payment',
                        type=float,
                        required=True)
    parser.add_argument('ss_deduction',
                        type=float,
                        required=False)
    parser.add_argument('se_deduction',
                        type=float,
                        required=False)
    parser.add_argument('isr_deduction',
                        type=float,
                        required=False)
    parser.add_argument('payment_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, detail_id):
        pmt_d = PaymentDetailModel.find_by_id(detail_id, current_identity)

        if pmt_d:
            return pmt_d.to_dict()

        return {'message': 'Payment detail not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = PaymentDetail.parser.parse_args()

        if PaymentModel.find_by_id(data['payment_id'], current_identity):
            pmt_d = PaymentDetailModel(**data)

            try:
                pmt_d.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the payment detail.'}, 500

            return {
                       'message': 'Payment detail created successfully.',
                       'payment_detail': PaymentDetailModel.find_by_id(
                           pmt_d.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create an payment detail'
                           'for an payment that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  detail_id):
        data = PaymentDetail.parser.parse_args()

        pmt_d = PaymentDetailModel.find_by_id(detail_id, current_identity)

        if pmt_d:
            try:
                _, pmt_d = pmt_d.update(data, ('payment_id',))
                return {
                   'message': 'Payment detail updated successfully.',
                   'payment_detail': pmt_d.to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the payment detail.'}, 500

        return {'message': 'Payment detail not found.'}, 404

    @jwt_required()
    def delete(self, detail_id):
        pmt_d = PaymentDetailModel.find_by_id(detail_id, current_identity)

        if pmt_d:
            try:
                pmt_d.delete_from_db()
                return {'message': 'Payment detail deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting'
                                   'the payment detail.'}, 500

        return {'message': 'Payment detail not found.'}, 404
