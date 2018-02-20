from flask_jwt import jwt_required
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
    def get(self, organization_name):
        organization = OrganizationModel.find_by_name(organization_name)
        if organization:
            return organization.to_dict(), 200

        return {'message': 'Organization not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Organization.parser.parse_args()

        if OrganizationModel.find_by_name(data['organization_name']):
            return {'message': 'An organization with that'
                               ' name already exists.'}, 400

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
                       organization.id
                   ).to_dict()
               }, 201

    @jwt_required()
    def put(self, organization_name):
        data = Organization.parser.parse_args()

        organization = OrganizationModel.find_by_name(organization_name)

        if organization:
            organization.organization_name = data['organization_name']

            try:
                organization.save_to_db()
                return {
                           'message': 'Organization updated successfully.',
                           'organization': OrganizationModel.find_by_id(
                               organization.id
                           ).to_dict()
                       }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the organization.'}, 500

        return {'message': 'Organization not found'}, 404

    @jwt_required()
    def delete(self, organization_name):
        organization = OrganizationModel.find_by_name(organization_name)

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
    def put(self, organization_name):
        organization = OrganizationModel.find_by_name(organization_name)

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


class OrganizationList(Resource):
    @jwt_required()
    def get(self):
        return {'organizations': list(map(lambda x: x.to_dict(),
                                          OrganizationModel.query.all()))}
