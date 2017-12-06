from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.user import UserModel


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
        user = UserModel.find_by_username(username)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    @staticmethod
    def post():
        data = User.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'],
                         data['password'],
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
