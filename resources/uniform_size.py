from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.uniform_item import UniformItemModel
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
        u_s = UniformSizeModel.find_by_id(size_id, current_identity)

        if u_s:
            return u_s.to_dict()

        return {'message': 'Uniform size not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = UniformSize.parser.parse_args()

        if UniformSizeModel.query.filter_by(
                size_description=data['size_description'],
                uniform_item_id=data['uniform_item_id']).first():
            return {'message': 'A uniform size with that description already '
                               'exists for that uniform item.'}, 400

        item = UniformItemModel.find_by_id(data['uniform_item_id'],
                                           current_identity)

        if item or current_identity.is_super:
            u_s = UniformSizeModel(**data)

            try:
                u_s.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the uniform size.'}, 500

            return {
                       'message': 'Uniform size created successfully.',
                       'uniform_size': UniformSizeModel.find_by_id(
                           u_s.id, current_identity).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create a uniform size for '
                           'an item that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  size_id):
        data = UniformSize.parser.parse_args()

        u_s = UniformSizeModel.find_by_id(size_id, current_identity)

        if u_s:
            try:
                _, u_s = u_s.update(data, ('uniform_item_id'))
                return {
                   'message': 'Uniform size updated successfully.',
                   'uniform_size': u_s.to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the uniform size.'}, 500

        return {'message': 'Uniform size not found.'}, 404

    @jwt_required()
    def delete(self, size_id):
        u_s = UniformSizeModel.find_by_id(size_id, current_identity)

        if u_s:
            try:
                u_s.delete_from_db()
                return {'message': 'Uniform size deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting '
                                   'the uniform size.'}, 500

        return {'message': 'Uniform size not found.'}, 404
