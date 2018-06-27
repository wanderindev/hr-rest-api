from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.creditor import CreditorModel
from models.organization import OrganizationModel


class Creditor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('creditor_name',
                        type=str,
                        required=True)
    parser.add_argument('phone_number',
                        type=str,
                        required=False)
    parser.add_argument('email',
                        type=str,
                        required=False)
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=False)
    parser.add_argument('organization_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, creditor_id):
        cred = CreditorModel.find_by_id(creditor_id, current_identity)

        if cred:
            return cred.to_dict()

        return {'message': 'Creditor not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Creditor.parser.parse_args()

        if CreditorModel.query.filter_by(
                creditor_name=data['creditor_name'],
                organization_id=data['organization_id']).first():
            return {'message': 'A creditor with that name already '
                               'exists in the organization.'}, 400

        if OrganizationModel.find_by_id(data['organization_id'],
                                        current_identity):
            cred = CreditorModel(**data)

            try:
                cred.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the creditor.'}, 500

            return {
                       'message': 'Creditor created successfully.',
                       'creditor': CreditorModel.find_by_id(
                           cred.id,
                           current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create a creditor that '
                           'does not belong to your organization.'}, 403

    @jwt_required()
    def put(self,  creditor_id):
        data = Creditor.parser.parse_args()

        cred = CreditorModel.find_by_id(creditor_id, current_identity)

        if cred:
            cred.creditor_name = data['creditor_name']
            cred.phone_number = data['phone_number']
            cred.email = data['email']

            try:
                _, cred = cred.update(data, ('is_active', 'organization_id'))
                return {
                   'message': 'Creditor updated successfully.',
                   'creditor': cred.to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the creditor.'}, 500

        return {'message': 'Creditor not found.'}, 404

    @jwt_required()
    def delete(self, creditor_id):
        cred = CreditorModel.find_by_id(creditor_id, current_identity)

        if cred:
            if cred.is_active:
                try:
                    cred.inactivate()
                    return {'message': 'Creditor is now inactive.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while inactivating'
                                       'the creditor.'}, 500
            else:
                return {'message': 'Creditor was already inactive.'}, 400

        return {'message': 'Creditor not found.'}, 404


class ActivateCreditor(Resource):
    @jwt_required()
    def put(self, creditor_id):
        cred = CreditorModel.find_by_id(creditor_id, current_identity)

        if cred:
            if not cred.is_active:
                try:
                    cred.activate()
                    return {'message': 'Creditor is now active.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while activating'
                                       'the creditor.'}, 500
            else:
                return {'message': 'Creditor was already active.'}, 400

        return {'message': 'Creditor not found.'}, 404
