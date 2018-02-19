from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.uniform_requirement import UniformRequirementModel


class UniformRequirement(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('employee_id',
                        type=int,
                        required=True)
    parser.add_argument('uniform_item_id',
                        type=int,
                        required=True)
    parser.add_argument('uniform_size_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, requirement_id):

        u_r = UniformRequirementModel\
            .find_by_id(requirement_id, current_identity.organization_id)
        if u_r:
            return u_r.to_dict()

        return {'message': 'Uniform requirement not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = UniformRequirement.parser.parse_args()

        if UniformRequirementModel.query\
                .filter_by(employee_id=data['employee_id'],
                           uniform_item_id=data['uniform_item_id'],
                           uniform_size_id=data['uniform_size_id']).first():
            return {'message': 'The uniform requirement already '
                               'exists in the database table.'}, 400

        u_r = UniformRequirementModel(data['employee_id'],
                                      data['uniform_item_id'],
                                      data['uniform_size_id'])

        try:
            u_r.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred creating '
                               'the uniform requirement.'}, 500

        return {
                   'message': 'Uniform requirement created successfully.',
                   'uniform_requirement': UniformRequirementModel.find_by_id(
                       u_r.id, current_identity.organization_id
                   ).to_dict()
               }, 201

    @jwt_required()
    def put(self,  requirement_id):
        data = UniformRequirement.parser.parse_args()

        u_r = UniformRequirementModel\
            .find_by_id(requirement_id,
                        current_identity.organization_id)

        if u_r:
            u_r.uniform_size_id = data['uniform_size_id']

            try:
                u_r.save_to_db()
                return {
                   'message': 'Uniform requirement updated successfully.',
                   'uniform_requirement': UniformRequirementModel.find_by_id(
                       u_r.id,
                       current_identity.organization_id
                   ).to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred updating '
                                   'the uniform requirement.'}, 500

        return {'message': 'Uniform requirement not found.'}, 404

    @jwt_required()
    def delete(self, requirement_id):
        u_r = UniformRequirementModel\
            .find_by_id(requirement_id,
                        current_identity.organization_id)

        if u_r:
            try:
                u_r.delete_from_db()
                return {'message': 'Uniform requirement deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting '
                                   'the uniform requirement.'}, 500

        return {'message': 'Uniform requirement not found.'}, 404
