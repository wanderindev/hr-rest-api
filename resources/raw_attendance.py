from flask import current_app, make_response
from flask_jwt import current_identity, jwt_required
from flask_restful import reqparse, Resource, request
from sqlalchemy.exc import SQLAlchemyError

from models.raw_attendance import RawAttendanceModel


class RawAttendance(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('stgid',
                        type=str,
                        required=False)
    parser.add_argument('userid',
                        type=int,
                        required=False)
    parser.add_argument('att_time',
                        type=int,
                        required=False)
    parser.add_argument('att_type',
                        type=str,
                        required=False)
    parser.add_argument('auth_token',
                        type=str,
                        required=False)

    @staticmethod
    def post():
        data = RawAttendance.parser.parse_args()

        if current_app.config['CLOCK_SECRETS'][data['stgid']] == \
                data['auth_token']:
            data.pop('auth_token')
            record = RawAttendanceModel(**data)

            try:
                record.save_to_db()
                resp = make_response('ok', 200,
                                     {'Content-Type': 'application/text'})
                return resp
            except SQLAlchemyError as e:
                return f'Ocurrió un error al tratar de crear el registro.  ' \
                       f'Error: "{e}"', 500, \
                       {'Content-Type': 'application/text'}

        return 'Token incorrecto.', 401, {'Content-Type': 'application/text'}


class RawAttendances(Resource):
    @jwt_required()
    def get(self):
        _list = RawAttendanceModel.find_all(current_identity)

        if _list:
            return {'list': list(map(lambda x: x.to_dict(), _list))}

        return {'message': 'Acceso denegado a listar este recurso.'}, 403
