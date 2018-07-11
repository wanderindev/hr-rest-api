from models.schedule import ScheduleModel
from resources.mixin import ListMixin, ResourceMixin


class Schedule(ResourceMixin):
    model = ScheduleModel
    parsed_model = model.parse_model()


class Schedules(ListMixin):
    model = ScheduleModel
