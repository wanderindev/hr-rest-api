from models.employee import EmployeeModel
from resources.mixin import ActivateMixin, ListMixin, ResourceMixin


class Employee(ResourceMixin):
    model = EmployeeModel
    parsed_model = model.parse_model()


class ActivateEmployee(ActivateMixin):
    model = EmployeeModel


class Employees(ListMixin):
    model = EmployeeModel