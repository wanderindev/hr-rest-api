from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.uniform_size import UniformSizeModel


class UniformSize(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('size_description',
                        type=str,
                        required=True)
    parser.add_argument('uniform_item_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, size_id):

        u_s = UniformSizeModel.find_by_id(size_id,
                                          current_identity.organization_id)
        if u_s:
            return u_s.to_dict()

        return {'message': 'Uniform size not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = UniformSize.parser.parse_args()

        if UniformSizeModel.find_by_description(data['size_description'],
                                                data['uniform_item_id'],
                                                current_identity.organization_id):
            return {'message': 'A uniform size with that description already '
                               'exists in that uniform item.'}, 400

        u_s = UniformSizeModel(data['size_description'],
                               data['uniform_item_id'])

        try:
            u_s.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred while creating '
                               'the uniform size.'}, 500

        return {
                   'message': 'Uniform size created successfully.',
                   'uniform_size': UniformSizeModel.find_by_id(
                       u_s.id, current_identity.organization_id
                   ).to_dict()
               }, 201

    @jwt_required()
    def put(self,  size_id):
        data = UniformSize.parser.parse_args()

        u_s = UniformSizeModel.find_by_id(size_id,
                                          current_identity.organization_id)

        if u_s:
            u_s.size_description = data['size_description']

            try:
                u_s.save_to_db()
                return {
                   'message': 'Uniform size updated successfully.',
                   'uniform_size': UniformSizeModel.find_by_id(
                       u_s.id,
                       current_identity.organization_id
                   ).to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the uniform size.'}, 500

        return {'message': 'Uniform size not found.'}, 404

    @jwt_required()
    def delete(self, size_id):
        u_s = UniformSizeModel.find_by_id(size_id,
                                          current_identity.organization_id)

        if u_s:
            try:
                u_s.delete_from_db()
                return {'message': 'Uniform size deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting '
                                   'the uniform size.'}, 500

        return {'message': 'Uniform size not found.'}, 404
