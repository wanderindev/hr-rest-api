from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.department import DepartmentModel
from models.employee import EmployeeModel


class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        required=True)
    parser.add_argument('second_name',
                        type=str,
                        required=False)
    parser.add_argument('first_surname',
                        type=str,
                        required=True)
    parser.add_argument('second_surname',
                        type=str,
                        required=False)
    parser.add_argument('national_id_number',
                        type=str,
                        required=False)
    parser.add_argument('is_panamanian',
                        type=bool,
                        required=True)
    parser.add_argument('date_of_birth',
                        type=str,
                        required=True)
    parser.add_argument('gender',
                        type=str,
                        required=True)
    parser.add_argument('address',
                        type=str,
                        required=True)
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=False)
    parser.add_argument('home_phone',
                        type=str,
                        required=False)
    parser.add_argument('mobile_phone',
                        type=str,
                        required=False)
    parser.add_argument('email',
                        type=str,
                        required=False)
    parser.add_argument('type_of_contract',
                        type=str,
                        required=True)
    parser.add_argument('employment_date',
                        type=str,
                        required=True)
    parser.add_argument('contract_expiration_date',
                        type=str,
                        required=False)
    parser.add_argument('termination_date',
                        type=str,
                        required=False)
    parser.add_argument('termination_reason',
                        type=str,
                        required=False)
    parser.add_argument('salary_per_payment_period',
                        type=float,
                        required=True)
    parser.add_argument('representation_expenses_per_payment_period',
                        type=float,
                        required=True)
    parser.add_argument('payment_method',
                        type=str,
                        required=False)
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=False)
    parser.add_argument('marital_status_id',
                        type=int,
                        required=True)
    parser.add_argument('department_id',
                        type=int,
                        required=True)
    parser.add_argument('position_id',
                        type=int,
                        required=True)
    parser.add_argument('shift_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, employee_id):

        empl = EmployeeModel.find_by_id(employee_id,
                                        current_identity.organization_id)

        if empl:
            return empl.to_dict()

        return {'message': 'Employee not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = Employee.parser.parse_args()

        if EmployeeModel.find_by_name(data['first_name'],
                                      data['second_name'],
                                      data['first_surname'],
                                      data['second_surname'],
                                      current_identity.organization_id):
            return {'message': 'An employee with that name already '
                               'exists in the organization.'}, 400

        if not DepartmentModel.find_by_id(data['department_id'],
                                          current_identity.organization_id):
            return {'message': 'You are not allowed to add an employee to a '
                               'department that does not belong to your'
                               'organization.'}, 403

        empl = EmployeeModel(data['first_name'],
                             data['second_name'],
                             data['first_surname'],
                             data['second_surname'],
                             data['national_id_number'],
                             data['is_panamanian'],
                             data['date_of_birth'],
                             data['gender'],
                             data['address'],
                             data['home_phone'],
                             data['mobile_phone'],
                             data['email'],
                             data['type_of_contract'],
                             data['employment_date'],
                             data['contract_expiration_date'],
                             data['termination_date'],
                             data['termination_reason'],
                             data['salary_per_payment_period'],
                             data['representation_expenses_per_payment_period'],
                             data['payment_method'],
                             data['is_active'],
                             data['marital_status_id'],
                             data['department_id'],
                             data['position_id'],
                             data['shift_id'])

        try:
            empl.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred creating '
                               'the employee.'}, 500

        return {
                   'message': 'Employee created successfully.',
                   'employee': EmployeeModel.find_by_id(
                       empl.id, current_identity.organization_id
                   ).to_dict()
               }, 201

    @jwt_required()
    def put(self,  employee_id):
        data = Employee.parser.parse_args()

        if not DepartmentModel.find_by_id(data['department_id'],
                                          current_identity.organization_id):
            return {'message': 'You are not allowed to move an employee to a '
                               'department that does not belong to your'
                               'organization.'}, 403

        empl = EmployeeModel.find_by_id(employee_id,
                                        current_identity.organization_id)

        if empl:
            empl.first_name = data['first_name']
            empl.second_name = data['second_name']
            empl.first_surname = data['first_surname']
            empl.second_surname = data['second_surname']
            empl.national_id_number = data['national_id_number']
            empl.is_panamanian = data['is_panamanian']
            empl.date_of_birth = data['date_of_birth']
            empl.gender = data['gender']
            empl.address = data['address']
            empl.home_phone = data['home_phone']
            empl.mobile_phone = data['mobile_phone']
            empl.email = data['email']
            empl.type_of_contract = data['type_of_contract']
            empl.employment_date = data['employment_date']
            empl.contract_expiration_date = data['contract_expiration_date']
            empl.termination_date = data['termination_date']
            empl.termination_reason = data['termination_reason']
            empl.salary_per_payment_period = data['salary_per_payment_period']
            empl.representation_expenses_per_payment_period = data[
                'representation_expenses_per_payment_period']
            empl.payment_method = data['payment_method']
            empl.marital_status_id = data['marital_status_id']
            empl.department_id = data['department_id']
            empl.position_id = data['position_id']
            empl.shift_id = data['shift_id']

            try:
                empl.save_to_db()
                return {
                           'message': 'Employee updated successfully.',
                           'employee': EmployeeModel.find_by_id(
                               empl.id, current_identity.organization_id
                           ).to_dict()
                       }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred updating '
                                   'the employee.'}, 500

        return {'message': 'Employee not found.'}, 404

    @jwt_required()
    def delete(self, employee_id):
        empl = EmployeeModel.find_by_id(employee_id,
                                        current_identity.organization_id)

        if empl:
            if empl.is_active:
                try:
                    empl.inactivate()
                    return {'message': 'Employee is now inactive.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while inactivating'
                                       'the employee.'}, 500
            else:
                return {'message': 'Employee was already inactive.'}, 400

        return {'message': 'Employee not found.'}, 404


class ActivateEmployee(Resource):
    @jwt_required()
    def put(self, employee_id):
        empl = EmployeeModel.find_by_id(employee_id,
                                        current_identity.organization_id)

        if empl:
            if not empl.is_active:
                try:
                    empl.activate()
                    return {'message': 'Employee is now active.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while activating'
                                       'the employee.'}, 500
            else:
                return {'message': 'Employee was already active.'}, 400

        return {'message': 'Employee not found.'}, 404
