from flask_jwt import jwt_required
from flask_restful import Resource


from models.marital_status import MaritalStatusModel


class MaritalStatusList(Resource):
    @jwt_required()
    def get(self):
        return {'marital_statuses': list(map(lambda x: x.to_dict(),
                                             MaritalStatusModel.query.all()))}
