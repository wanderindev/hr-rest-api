from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.bank_account import BankAccountModel
from models.employee import EmployeeModel


class BankAccount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('account_number',
                        type=str,
                        required=True)
    parser.add_argument('account_type',
                        type=str,
                        required=True)
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=False)
    parser.add_argument('employee_id',
                        type=int,
                        required=True)
    parser.add_argument('bank_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, account_id):

        b_acc = BankAccountModel.find_by_id(account_id, current_identity)
        if b_acc:
            return b_acc.to_dict()

        return {'message': 'Bank account not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = BankAccount.parser.parse_args()

        if BankAccountModel.query.filter_by(
                account_number=data['account_number'],
                account_type=data['account_type'],
                bank_id=data['bank_id']).first():
            return {'message': 'A bank account with same number and bank_id '
                               'already exists.'}, 400

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            b_acc = BankAccountModel(data['account_number'],
                                     data['account_type'],
                                     data['is_active'],
                                     data['employee_id'],
                                     data['bank_id'])

            try:
                b_acc.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the bank_account.'}, 500

            return {
                       'message': 'Bank account created successfully.',
                       'bank_account': BankAccountModel.find_by_id(
                           b_acc.id, current_identity
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create a bank account '
                           'for an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def put(self,  account_id):
        data = BankAccount.parser.parse_args()

        if BankAccountModel.query.filter_by(
                account_number=data['account_number'],
                account_type=data['account_type'],
                bank_id=data['bank_id']).first():
            return {'message': 'A bank account with same number and bank_id '
                               'already exists.'}, 400

        if EmployeeModel.find_by_id(data['employee_id'], current_identity):
            b_acc = BankAccountModel.find_by_id(account_id, current_identity)

            if b_acc:
                b_acc.account_number = data['account_number']
                b_acc.account_type = data['account_type']
                b_acc.bank_id = data['bank_id']

                try:
                    b_acc.save_to_db()
                    return {
                       'message': 'Bank account updated successfully.',
                       'bank_account': BankAccountModel.find_by_id(
                           b_acc.id, current_identity
                       ).to_dict()
                    }, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while updating '
                                       'the bank_account.'}, 500

            return {'message': 'Bank account not found.'}, 404

        return {'message': 'You are not allowed to modify a bank account '
                           'for an employee that does not belong to your '
                           'organization.'}, 403

    @jwt_required()
    def delete(self, account_id):
        b_acc = BankAccountModel.find_by_id(account_id, current_identity)

        if b_acc:
            if b_acc.is_active:
                try:
                    b_acc.inactivate()
                    return {'message': 'Bank account is now inactive.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while inactivating'
                                       'the bank_account.'}, 500
            else:
                return {'message': 'Bank account was already inactive.'}, 400

        return {'message': 'Bank account not found.'}, 404


class ActivateBankAccount(Resource):
    @jwt_required()
    def put(self, account_id):
        b_acc = BankAccountModel.find_by_id(account_id, current_identity)

        if b_acc:
            if not b_acc.is_active:
                try:
                    b_acc.activate()
                    return {'message': 'Bank account is now active.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while activating'
                                       'the bank_account.'}, 500
            else:
                return {'message': 'Bank account was already active.'}, 400

        return {'message': 'Bank account not found.'}, 404
