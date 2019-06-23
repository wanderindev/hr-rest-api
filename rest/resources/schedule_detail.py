from models.schedule_detail import ScheduleDetailModel
from resources.mixin import ListMixin, ResourceMixin


class ScheduleDetail(ResourceMixin):
    model = ScheduleDetailModel
    parsed_model = model.parse_model()


class ScheduleDetails(ListMixin):
    model = ScheduleDetailModel
