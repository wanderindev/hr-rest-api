from flask_jwt import jwt_required
from flask_restful import Resource


from models.family_relation import FamilyRelationModel


class FamilyRelationList(Resource):
    @jwt_required()
    def get(self):
        return {'family_relations': list(map(lambda x: x.to_dict(),
                                            FamilyRelationModel.find_all()))}
