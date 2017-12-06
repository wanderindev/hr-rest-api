from flask_jwt import jwt_required
from flask_restful import reqparse, Resource
from sqlalchemy import exc

from models.organization import OrganizationModel


class Organization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True)
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=False)

    @jwt_required()
    def get(self, name):
        organization = OrganizationModel.find_by_name(name)
        if organization:
            return organization.json()
        return {'message': 'Organization not found'}, 404

    @staticmethod
    def post():
        data = Organization.parser.parse_args()

        if OrganizationModel.find_by_name(data['name']):
            return {'message': "An organization with name '{}'"
                               " already exists.".format(data['name'])}, 400

        organization = OrganizationModel(data['name'], data['is_active'])
        try:
            organization.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred creating '
                               'the organization.'}, 500

        return organization.json(), 201


class OrganizationList(Resource):
    @jwt_required()
    def get(self):
        return {'organization': list(map(lambda x: x.json(),
                                         OrganizationModel.query.all()))}
