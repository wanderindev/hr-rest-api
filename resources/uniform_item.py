from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.uniform_item import UniformItemModel


class UniformItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('item_name',
                        type=str,
                        required=True)
    parser.add_argument('organization_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, item_id):
        u_i = UniformItemModel.find_by_id(item_id, current_identity)
        if u_i:
            return u_i.to_dict()

        return {'message': 'Uniform item not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = UniformItem.parser.parse_args()

        if UniformItemModel.query.filter_by(
                item_name=data['item_name'],
                organization_id=data['organization_id']).first():
            return {'message': 'A uniform item with that name already '
                               'exists in the organization.'}, 400

        if current_identity.organization_id == data['organization_id'] or \
                current_identity.is_super:
            u_i = UniformItemModel(**data)

            try:
                u_i.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the uniform item.'}, 500

            return {
                       'message': 'Uniform item created successfully.',
                       'uniform_item': UniformItemModel.find_by_id(
                           u_i.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create a uniform item '
                           'that does not belong to your organization.'}, 403

    @jwt_required()
    def put(self,  item_id):
        data = UniformItem.parser.parse_args()

        u_i = UniformItemModel.find_by_id(item_id, current_identity)

        if u_i:
            try:
                _, u_i = u_i.update(data, ['organization_id'])
                return {
                   'message': 'Uniform item updated successfully.',
                   'uniform_item': u_i.to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the uniform item.'}, 500

        return {'message': 'Uniform item not found.'}, 404

    @jwt_required()
    def delete(self, item_id):
        u_i = UniformItemModel.find_by_id(item_id, current_identity)

        if u_i:
            try:
                u_i.delete_from_db()
                return {'message': 'Uniform item deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting '
                                   'the uniform item.'}, 500

        return {'message': 'Uniform item not found.'}, 404
