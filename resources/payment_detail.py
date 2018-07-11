from models.payment_detail import PaymentDetailModel
from resources.mixin import ListMixin, ResourceMixin


class PaymentDetail(ResourceMixin):
    model = PaymentDetailModel
    parsed_model = model.parse_model()


class PaymentDetails(ListMixin):
    model = PaymentDetailModel
