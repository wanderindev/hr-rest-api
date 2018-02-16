from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.emergency_contact import EmergencyContactModel


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

        e_cont = EmergencyContactModel.find_by_id(
            contact_id, current_identity.organization_id)
        if e_cont:
            return e_cont.to_dict()

        return {'message': 'Emergency contact not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = EmergencyContact.parser.parse_args()

        e_cont = EmergencyContactModel(data['first_name'],
                                       data['last_name'],
                                       data['home_phone'],
                                       data['work_phone'],
                                       data['mobile_phone'],
                                       data['employee_id'])

        try:
            e_cont.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred creating '
                               'the emergency contact.'}, 500

        return {
                   'message': 'Emergency contact created successfully.',
                   'emergency_contact': EmergencyContactModel.find_by_id(
                       e_cont.id, current_identity.organization_id
                   ).to_dict()
               }, 201

    @jwt_required()
    def put(self,  contact_id):
        data = EmergencyContact.parser.parse_args()

        e_cont = EmergencyContactModel.find_by_id(
            contact_id, current_identity.organization_id)

        if e_cont:
            e_cont.first_name = data['first_name']
            e_cont.last_name = data['last_name']
            e_cont.home_phone = data['home_phone']
            e_cont.work_phone = data['work_phone']
            e_cont.mobile_phone = data['mobile_phone']
            e_cont.employee_id = data['employee_id']

            try:
                e_cont.save_to_db()
                return {
                   'message': 'Emergency contact updated successfully.',
                   'emergency_contact': EmergencyContactModel.find_by_id(
                       e_cont.id, current_identity.organization_id
                   ).to_dict()
                }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred updating '
                                   'the emergency contact.'}, 500

        return {'message': 'Emergency contact not found.'}, 404

    @jwt_required()
    def delete(self, contact_id):
        e_cont = EmergencyContactModel.find_by_id(
            contact_id, current_identity.organization_id)

        if e_cont:
            try:
                e_cont.delete_from_db()
                return {'message': 'Emergency contact deleted.'}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while deleting'
                                   'the emergency contact.'}, 500

        return {'message': 'Emergency contact not found.'}, 404
