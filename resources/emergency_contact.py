from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.emergency_contact import EmergencyContactModel
from models.employee import EmployeeModel


class EmergencyContact(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        required=True)
    parser.add_argument('last_name',
                        type=str,
                        required=True)
    parser.add_argument('home_phone',
                        type=str,
                        required=False)
    parser.add_argument('work_phone',
                        type=str,
                        required=False)
    parser.add_argument('mobile_phone',
                        type=str,
                        required=False)
    parser.add_argument('employee_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, contact_id):
        e_cont = EmergencyContactModel.find_by_id(contact_id, current_identity)

        if e_cont:
            return e_cont.to_dict()

        return {'message': 'Emergency contact not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = EmergencyContact.parser.parse_args()

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            e_cont = EmergencyContactModel(**data)

            try:
                e_cont.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the emergency contact.'}, 500

            return {
                       'message': 'Emergency contact created successfully.',
                       'emergency_contact': EmergencyContactModel.find_by_id(
                           e_cont.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create an emergency contact '
                           'for an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  contact_id):
        data = EmergencyContact.parser.parse_args()

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            e_cont = EmergencyContactModel.find_by_id(contact_id,
                                                      current_identity)

            if e_cont:
                try:
                    _, e_cont = e_cont.update(data)
                    return {
                       'message': 'Emergency contact updated successfully.',
                       'emergency_contact': e_cont.to_dict()
                    }, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while updating '
                                       'the emergency contact.'}, 500

            return {'message': 'Emergency contact not found.'}, 404

        return {'message': 'You are not allowed to assign an emergency contact '
                           'to an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def delete(self, contact_id):
        e_cont = EmergencyContactModel.find_by_id(contact_id, current_identity)

        if e_cont:
            try:
                e_cont.delete_from_db()
                return {'message': 'Emergency contact deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting'
                                   'the emergency contact.'}, 500

        return {'message': 'Emergency contact not found.'}, 404
