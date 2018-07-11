from models.deduction_detail import DeductionDetailModel
from resources.mixin import ListMixin, ResourceMixin


class DeductionDetail(ResourceMixin):
    model = DeductionDetailModel
    parsed_model = model.parse_model()


class DeductionDetails(ListMixin):
    model = DeductionDetailModel
