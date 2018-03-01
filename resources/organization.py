from flask_jwt import current_identity, jwt_required
from flask_restful import reqparse, Resource
from sqlalchemy import exc

from models.organization import OrganizationModel


class Organization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('organization_name',
                        type=str,
                        required=True)
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=False)

    @jwt_required()
    def get(self, organization_id):
        organization = OrganizationModel.find_by_id(organization_id,
                                                    current_identity)
        if organization:
            return organization.to_dict(), 200

        return {'message': 'Organization not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Organization.parser.parse_args()

        if not current_identity.is_super:
            return {'message': 'You are not allowed to create '
                               'new organizations.'}, 403

        if OrganizationModel.query.filter_by(
                organization_name=data['organization_name']).first():
            return {'message': 'An organization with that '
                               'name already exists.'}, 400

        organization = OrganizationModel(
            data['organization_name'],
            data['is_active'])

        try:
            organization.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred while creating '
                               'the organization.'}, 500

        return {
                   'message': 'Organization created successfully.',
                   'organization': OrganizationModel.find_by_id(
                       organization.id,
                       current_identity
                   ).to_dict()
               }, 201

    @jwt_required()
    def put(self, organization_id):
        data = Organization.parser.parse_args()

        organization = OrganizationModel.find_by_id(organization_id,
                                                    current_identity)

        if organization:
            organization.organization_name = data['organization_name']

            try:
                organization.save_to_db()
                return {
                           'message': 'Organization updated successfully.',
                           'organization': OrganizationModel.find_by_id(
                               organization.id,
                               current_identity
                           ).to_dict()
                       }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the organization.'}, 500

        return {'message': 'Organization not found'}, 404

    @jwt_required()
    def delete(self, organization_id):
        if not current_identity.is_super:
            return {'message': 'You are not allowed to inactivate '
                               'an organization.'}, 403

        organization = OrganizationModel.find_by_id(organization_id,
                                                    current_identity)

        if organization:
            if organization.is_active:
                try:
                    organization.inactivate()
                    return {'message': 'Organization is now inactive.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while inactivating'
                                       'the organization.'}, 500
            else:
                return {'message': 'Organization was already inactive.'}, 400

        return {'message': 'Organization not found.'}, 404


class ActivateOrganization(Resource):
    @jwt_required()
    def put(self, organization_id):
        if not current_identity.is_super:
            return {'message': 'You are not allowed to activate '
                               'an organization.'}, 403

        organization = OrganizationModel.find_by_id(organization_id,
                                                    current_identity)

        if organization:
            if not organization.is_active:
                try:
                    organization.activate()
                    return {'message': 'Organization is now active.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while activating'
                                       'the organization.'}, 500
            else:
                return {'message': 'Organization was already active.'}, 400

        return {'message': 'Organization not found.'}, 404


class Organizations(Resource):
    @jwt_required()
    def get(self):
        if current_identity.is_super:
            return {'organizations': list(map(lambda x: x.to_dict(),
                                              OrganizationModel.query.all()))}

        return {'message': 'You are not allowed to view the list of'
                           'organizations.'}, 403
