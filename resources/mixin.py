from flask_jwt import current_identity, jwt_required
from flask_restful import reqparse, Resource
from sqlalchemy.exc import SQLAlchemyError


class ResourceMixin(Resource):
    def get_parser(self):
        parser = reqparse.RequestParser()

        for key in self.parsed_model['keys']:
            if key is not 'password_hash':
                is_required = key not in self.parsed_model['nullable']
                if key in self.parsed_model['int']:
                    parser.add_argument(key,
                                        type=int,
                                        required=is_required)
                elif key in self.parsed_model['float']:
                    parser.add_argument(key,
                                        type=float,
                                        required=is_required)
                elif key in self.parsed_model['bool']:
                    parser.add_argument(key,
                                        type=bool,
                                        required=is_required)
                else:
                    parser.add_argument(key,
                                        type=str,
                                        required=is_required)

        return parser

    @jwt_required()
    def get(self, _id):
        record = self.model.find_by_id(_id, current_identity)

        if record:
            return {'record': record.to_dict()}, 200

        return {'message': 'El registro solicitado no existe.'}, 404

    @jwt_required()
    def post(self):
        parser = self.get_parser()
        data = parser.parse_args()

        if self.parsed_model['unique']:
            for constraint in self.parsed_model['unique']:
                _filter = {}
                for key in constraint:
                    _filter[key] = data[key]

                if self.model.query.filter_by(**_filter).first():
                    return {'message': f'El valor "{_filter}" viola '
                                       f'UNIQUE_CONSTRAINT de la tabla'}, 400

        record = self.model(**data)

        try:
            record.save_to_db()
            if 'stgid' in data:
                return 'ok', 201
            return {
                       'message': 'Registro creado exitosamente.',
                       'record': self.model.find_by_id(
                           record.id,
                           current_identity
                       ).to_dict()
                   }, 201
        except SQLAlchemyError as e:
            return {'message': f'Ocurrió un error al tratar de crear '
                               f'el registro.  Error: "{e}"'}, 500

    @jwt_required()
    def put(self, _id):
        parser = self.get_parser()
        data = parser.parse_args()

        if self.parsed_model['unique']:
            for constraint in self.parsed_model['unique']:
                _filter = {}
                for key in constraint:
                    _filter[key] = data[key]

                if self.model.query.filter_by(**_filter).first() and \
                        self.model.query.filter_by(**_filter)\
                        .first().id != _id:
                    return {'message': f'El valor "{_filter}" viola '
                                       f'UNIQUE_CONSTRAINT de la tabla'}, 400

        record = self.model.find_by_id(_id, current_identity)

        if record:
            try:
                _, rec = record.update(data)
                return {
                           'message': 'Registro actualizado exitosamente.',
                           'record': rec.to_dict()
                       }, 200
            except SQLAlchemyError as e:
                return {'message': f'Ocurrió un error al tratar de modificar '
                                   f'el registro.  Error: "{e}"'}, 500

        return {'message': 'El registro solicitado no existe.'}, 404

    @jwt_required()
    def delete(self, _id):
        record = self.model.find_by_id(_id, current_identity)

        if record:
            try:
                record.delete_from_db()
                return {'message': 'El registro fue eliminado.'}, 200
            except SQLAlchemyError as e:
                return {'message': f'Ocurrió un error al tratar de eliminar '
                                   f'el registro.  Error: "{e}"'}, 500

        return {'message': 'El registro solicitado no existe.'}, 404


class ActivateMixin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('is_active',
                        type=bool,
                        required=True)

    @jwt_required()
    def put(self, _id):
        data = self.parser.parse_args()

        record = self.model.find_by_id(_id, current_identity)

        if record:
            if data['is_active']:
                if not record.is_active:
                    try:
                        record.activate()
                        return {'message': 'El registro fue activado.'}, 200
                    except SQLAlchemyError as e:
                        return {'message': f'Ocurrió un error al tratar de '
                                           f'activar el registro.  Error: '
                                           f'"{e}"'}, 500
                else:
                    return {'message': 'El registro ya estaba activo.'}, 400
            else:
                if record.is_active:
                    try:
                        record.inactivate()
                        return {'message': 'El registro fue inactivado.'}, 200
                    except SQLAlchemyError as e:
                        return {'message': f'Ocurrió un error al tratar de '
                                           f'inactivar el registro.  Error: '
                                           f'"{e}"'}, 500
                else:
                    return {'message': 'El registro ya estaba inactivo.'}, 400

        return {'message': 'El registro solicitado no existe.'}, 404


class ListMixin(Resource):
    @jwt_required()
    def get(self, _id=None):
        if _id:
            _list = self.model.find_all(current_identity, _id)
        else:
            _list = self.model.find_all(current_identity)

        if _list:
            return {'list': list(map(lambda x: x.to_dict(), _list))}

        return {'message': 'Acceso denegado a listar este recurso.'}, 403
