from models.attendance import AttendanceModel
from resources.mixin import ListMixin, ResourceMixin


class Attendance(ResourceMixin):
    model = AttendanceModel
    parsed_model = model.parse_model()


class Attendances(ListMixin):
    model = AttendanceModel
