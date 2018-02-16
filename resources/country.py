from flask_jwt import jwt_required
from flask_restful import Resource


from models.country import CountryModel


class CountryList(Resource):
    @jwt_required()
    def get(self):
        return {'countries': list(map(lambda x: x.to_dict(),
                                      CountryModel.find_all()))}
