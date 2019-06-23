from models.department import DepartmentModel
from resources.mixin import ActivateMixin, ListMixin, ResourceMixin


class Department(ResourceMixin):
    model = DepartmentModel
    parsed_model = model.parse_model()


class ActivateDepartment(ActivateMixin):
    model = DepartmentModel


class Departments(ListMixin):
    model = DepartmentModel
