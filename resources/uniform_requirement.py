from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.employee import EmployeeModel
from models.uniform_item import UniformItemModel
from models.uniform_requirement import UniformRequirementModel
from models.uniform_size import UniformSizeModel


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
        u_r = UniformRequirementModel.find_by_id(requirement_id,
                                                 current_identity)
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

        if not EmployeeModel.find_by_id(data['employee_id'], current_identity):
            return {'message': 'You are not allowed access to that '
                               'employee.'}, 403

        if not UniformItemModel.find_by_id(data['uniform_item_id'],
                                           current_identity):
            return {'message': 'You are not allowed access to that '
                               'uniform item.'}, 403

        u_s = UniformSizeModel.find_by_id(data['uniform_size_id'],
                                          current_identity)

        if not u_s.uniform_item_id == data['uniform_item_id']:
            return {'message': 'The uniform size does not belong to that '
                               'uniform item.'}, 400

        u_r = UniformRequirementModel(**data)

        try:
            u_r.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred while creating '
                               'the uniform requirement.'}, 500

        return {
                   'message': 'Uniform requirement created '
                              'successfully.',
                   'uniform_requirement': UniformRequirementModel.find_by_id(
                       u_r.id, current_identity).to_dict()
               }, 201

    @jwt_required()
    def put(self,  requirement_id):
        data = UniformRequirement.parser.parse_args()

        u_s = UniformSizeModel.find_by_id(data['uniform_size_id'],
                                          current_identity)
        if u_s.uniform_item_id == data['uniform_item_id']:
            u_r = UniformRequirementModel.find_by_id(requirement_id,
                                                     current_identity)

            if u_r:
                try:
                    _, u_r = u_r.update(data, ('employee_id, uniform_item_id'))
                    return {
                       'message': 'Uniform requirement updated successfully.',
                       'uniform_requirement': u_r.to_dict()
                    }, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while updating '
                                       'the uniform requirement.'}, 500

            return {'message': 'Uniform requirement not found.'}, 404

        return {'message': 'The uniform size does not belong to that '
                           'uniform item.'}, 400

    @jwt_required()
    def delete(self, requirement_id):
        u_r = UniformRequirementModel.find_by_id(requirement_id,
                                                 current_identity)

        if u_r:
            try:
                u_r.delete_from_db()
                return {'message': 'Uniform requirement deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting '
                                   'the uniform requirement.'}, 500

        return {'message': 'Uniform requirement not found.'}, 404
