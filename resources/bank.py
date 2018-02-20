from flask_jwt import jwt_required
from flask_restful import Resource

from models.bank import BankModel


class BankList(Resource):
    @jwt_required()
    def get(self):
        return {'banks': list(map(lambda x: x.to_dict(),
                                  BankModel.find_all()))}
