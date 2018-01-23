from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.user import AppUserModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('is_super',
                        default=False,
                        type=bool,
                        required=False)
    parser.add_argument('is_owner',
                        default=False,
                        type=bool,
                        required=False)
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=False)
    parser.add_argument('organization_id',
                        type=int,
                        required=True,
                        help="A user must belong to an organization")

    @jwt_required()
    def get(self, username):
        user = AppUserModel.find_by_username(username)
        if user:
            return user.to_dict()
        return {'message': 'User not found'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = User.parser.parse_args()

        if AppUserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = AppUserModel(data['username'],
                            data['password'],
                            data['email'],
                            data['organization_id'],
                            data['is_super'],
                            data['is_owner'],
                            data['is_active'])

        try:
            user.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred creating '
                               'the user.'}, 500

        return {"message": "User created successfully."}, 201

    @jwt_required()
    def put(self, username):
        data = User.parser.parse_args()

        user = AppUserModel.find_by_username(username)

        if user:
            user.username = data['username']
            user.set_password_hash(data['password'])
            user.email = data['email']
            user.is_super = data['is_super']
            user.is_owner = data['is_owner']

            try:
                user.save_to_db()
                return {"message": "User updated successfully."}, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred updating '
                                   'the user.'}, 500
        else:
            return {'message': 'User not found'}, 404

    @jwt_required()
    def delete(self, username):
        user = AppUserModel.find_by_username(username)

        if user:
            if user.is_active:
                try:
                    user.inactivate()
                    return {"message": "User is now inactive."}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while inactivating'
                                       'the user.'}, 500
            else:
                return {'message': 'User was already inactive.'}, 400
        else:
            return {'message': 'User not found'}, 404


class ActivateUser(Resource):
    @jwt_required()
    def put(self, username):
        user = AppUserModel.find_by_username(username)

        if user:
            if not user.is_active:
                try:
                    user.activate()
                    return {"message": "User is now active."}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while activating'
                                       'the user.'}, 500
            else:
                return {'message': 'User was already active.'}, 400
        else:
            return {'message': 'User not found'}, 404
