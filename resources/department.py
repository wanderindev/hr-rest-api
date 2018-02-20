from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.department import DepartmentModel


class Department(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('department_name',
                        type=str,
                        required=True)
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=False)
    parser.add_argument('organization_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, department_name):

        dept = DepartmentModel.find_by_name(department_name,
                                            current_identity.organization_id)
        if dept:
            return dept.to_dict()

        return {'message': 'Department not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Department.parser.parse_args()

        if DepartmentModel.find_by_name(data['department_name'],
                                        data['organization_id']):
            return {'message': 'A department with that name already '
                               'exists in the organization.'}, 400

        dept = DepartmentModel(data['department_name'],
                               data['organization_id'],
                               data['is_active'])

        try:
            dept.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred while creating '
                               'the department.'}, 500

        return {
                   'message': 'Department created successfully.',
                   'department': DepartmentModel.find_by_id(
                       dept.id, current_identity.organization_id
                   ).to_dict()
               }, 201

    @jwt_required()
    def put(self,  department_name):
        data = Department.parser.parse_args()

        dept = DepartmentModel.find_by_name(department_name,
                                            current_identity.organization_id)

        if dept:
            dept.department_name = data['department_name']

            try:
                dept.save_to_db()
                return {
                   'message': 'Department updated successfully.',
                   'department': DepartmentModel.find_by_id(
                       dept.id, current_identity.organization_id
                   ).to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the department.'}, 500

        return {'message': 'Department not found.'}, 404

    @jwt_required()
    def delete(self, department_name):
        dept = DepartmentModel.find_by_name(department_name,
                                            current_identity.organization_id)

        if dept:
            if dept.is_active:
                try:
                    dept.inactivate()
                    return {'message': 'Department is now inactive.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while inactivating'
                                       'the department.'}, 500
            else:
                return {'message': 'Department was already inactive.'}, 400

        return {'message': 'Department not found.'}, 404


class ActivateDepartment(Resource):
    @jwt_required()
    def put(self, department_name):
        dept = DepartmentModel.find_by_name(department_name,
                                            current_identity.organization_id)

        if dept:
            if not dept.is_active:
                try:
                    dept.activate()
                    return {'message': 'Department is now active.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while activating'
                                       'the department.'}, 500
            else:
                return {'message': 'Department was already active.'}, 400

        return {'message': 'Department not found.'}, 404
