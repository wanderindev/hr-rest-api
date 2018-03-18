from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.department import DepartmentModel
from models.organization import OrganizationModel


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
    def get(self, department_id):
        dept = DepartmentModel.find_by_id(department_id, current_identity)

        if dept:
            return dept.to_dict()

        return {'message': 'Department not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Department.parser.parse_args()

        if DepartmentModel.query.filter_by(
                department_name=data['department_name'],
                organization_id=data['organization_id']).first():
            return {'message': 'A department with that name already '
                               'exists in the organization.'}, 400

        if OrganizationModel.find_by_id(data['organization_id'],
                                        current_identity):
            dept = DepartmentModel(**data)

            try:
                dept.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the department.'}, 500

            return {
                       'message': 'Department created successfully.',
                       'department': DepartmentModel.find_by_id(
                           dept.id,
                           current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create a department that '
                           'does not belong to your organization.'}, 403

    @jwt_required()
    def put(self,  department_id):
        data = Department.parser.parse_args()

        dept = DepartmentModel.find_by_id(department_id, current_identity)

        if dept:
            dept.department_name = data['department_name']

            try:
                _, dept = dept.update(data, ['is_active', 'organization_id'])
                return {
                   'message': 'Department updated successfully.',
                   'department': dept.to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the department.'}, 500

        return {'message': 'Department not found.'}, 404

    @jwt_required()
    def delete(self, department_id):
        dept = DepartmentModel.find_by_id(department_id, current_identity)

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
    def put(self, department_id):
        dept = DepartmentModel.find_by_id(department_id, current_identity)

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
