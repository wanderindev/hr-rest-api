from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.department import DepartmentModel


class Department(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('department_name',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=False)
    parser.add_argument('organization_id',
                        type=int,
                        required=True,
                        help='A deparment must belong to an organization')

    @jwt_required()
    def get(self, department_name, organization_id):
        dept = DepartmentModel.find_by_name(department_name, organization_id)
        if dept:
            return dept.to_dict()
        return {'message': 'Department not found'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Department.parser.parse_args()

        if DepartmentModel.find_by_name(data['department_name'],
                                        data['organization_id']):
            return {'message': 'A department with that name already '
                               'exists in the organization'}, 400

        dept = DepartmentModel(data['department_name'],
                               data['organization_id'],
                               data['is_active'])

        try:
            dept.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred creating '
                               'the department.'}, 500

        return {'message': 'Department created successfully.'}, 201

    @jwt_required()
    def put(self,  department_name, organization_id):
        data = Department.parser.parse_args()

        dept = DepartmentModel.find_by_name(department_name, organization_id)

        if dept:
            dept.department_name = data['department_name']

            try:
                dept.save_to_db()
                return {'message': 'Department updated successfully.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred updating '
                                   'the department.'}, 500
        else:
            return {'message': 'Department not found'}, 404

    @jwt_required()
    def delete(self, department_name, organization_id):
        dept = DepartmentModel.find_by_name(department_name, organization_id)

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
        else:
            return {'message': 'Department not found'}, 404


class ActivateDepartment(Resource):
    @jwt_required()
    def put(self, department_name, organization_id):
        dept = DepartmentModel.find_by_name(department_name, organization_id)

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
        else:
            return {'message': 'Department not found'}, 404
