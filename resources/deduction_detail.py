from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.deduction import DeductionModel
from models.deduction_detail import DeductionDetailModel


class DeductionDetail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('deducted_amount',
                        type=float,
                        required=True)
    parser.add_argument('payment_id',
                        type=int,
                        required=True)
    parser.add_argument('deduction_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, detail_id):
        d_d = DeductionDetailModel.find_by_id(detail_id, current_identity)

        if d_d:
            return d_d.to_dict()

        return {'message': 'Deduction detail not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = DeductionDetail.parser.parse_args()

        if DeductionModel.find_by_id(data['deduction_id'], current_identity):
            d_d = DeductionDetailModel(**data)

            try:
                d_d.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the deduction detail.'}, 500

            return {
                       'message': 'Deduction detail created successfully.',
                       'deduction_detail': DeductionDetailModel.find_by_id(
                           d_d.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create an deduction detail '
                           'for an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  detail_id):
        data = DeductionDetail.parser.parse_args()

        d_d = DeductionDetailModel.find_by_id(detail_id, current_identity)

        if d_d:
            try:
                _, d_d = d_d.update(data)
                return {
                   'message': 'Deduction detail updated successfully.',
                   'deduction_detail': d_d.to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the deduction detail.'}, 500

        return {'message': 'Deduction detail not found.'}, 404

    @jwt_required()
    def delete(self, detail_id):
        d_d = DeductionDetailModel.find_by_id(detail_id, current_identity)

        if d_d:
            try:
                d_d.delete_from_db()
                return {'message': 'Deduction detail deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting'
                                   'the deduction detail.'}, 500

        return {'message': 'Deduction detail not found.'}, 404
