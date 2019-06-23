from models.payment import PaymentModel
from resources.mixin import ListMixin, ResourceMixin


class Payment(ResourceMixin):
    model = PaymentModel
    parsed_model = model.parse_model()


class Payments(ListMixin):
    model = PaymentModel
