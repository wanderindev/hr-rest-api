from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.attendance import Attendance, Attendances
from resources.bank import Banks
from resources.bank_account import ActivateBankAccount, BankAccount, \
    BankAccounts
from resources.country import Countries
from resources.creditor import ActivateCreditor, Creditor, Creditors
from resources.deduction import ActivateDeduction, Deduction, Deductions
from resources.deduction_detail import DeductionDetail, DeductionDetails
from resources.department import ActivateDepartment, Department, Departments
from resources.dependent import Dependent, Dependents
from resources.emergency_contact import EmergencyContact, EmergencyContacts
from resources.employee import ActivateEmployee, Employee, Employees
from resources.employment_position import ActivateEmploymentPosition, \
    EmploymentPosition, EmploymentPositions
from resources.family_relation import FamilyRelations
from resources.health_permit import HealthPermit, HealthPermits
from resources.marital_status import MaritalStatuses
from resources.organization import ActivateOrganization, Organization, \
    Organizations
from resources.passport import Passport, Passports
from resources.payment import Payment, Payments
from resources.payment_detail import PaymentDetail, PaymentDetails
from resources.schedule import Schedule, Schedules
from resources.schedule_detail import ScheduleDetail, ScheduleDetails
from resources.shift import ActivateShift, Shift, Shifts
from resources.uniform_item import UniformItem, UniformItems
from resources.uniform_requirement import UniformRequirement, \
    UniformRequirements
from resources.uniform_size import UniformSize, UniformSizes
from resources.user import ActivateUser, User, Users
from security import authenticate, identity


# noinspection PyTypeChecker
def create_app(config_file=None):
    """
    App factory for the creation of a Flask app.

    Creates a Flask app.  The app configuration is set from the
    file passed-in as an argument.  The file must be located
    within the config folder.

    Secret or sensitive configuration settings should be placed
    in the 'instance/settings.py' file which should be kept out
    of version control.

    :param config_file: The name of the file (without .py) within the
        'config' folder which has the configuration values.
    :return: A Flask app instance.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Load config settings for development or testing.
    if config_file:
        app.config.from_object(f'config.{config_file}')

    # Apply production settings, if available.
    app.config.from_pyfile('settings.py', silent=True)

    # Register the extensions.
    JWT(app, authenticate, identity)
    api = Api(app)

    # Add API resources.
    api.add_resource(Organization,
                     '/organization',
                     '/organization/<int:_id>')
    api.add_resource(ActivateOrganization,
                     '/activate_organization/<int:_id>')
    api.add_resource(Organizations,
                     '/organizations')

    api.add_resource(User,
                     '/user',
                     '/user/<int:_id>')
    api.add_resource(ActivateUser,
                     '/activate_user/<int:_id>')
    api.add_resource(Users,
                     '/users')

    api.add_resource(Department,
                     '/department',
                     '/department/<int:_id>')
    api.add_resource(ActivateDepartment,
                     '/activate_department/<int:_id>')
    api.add_resource(Departments,
                     '/departments')

    api.add_resource(MaritalStatuses,
                     '/marital_statuses')

    api.add_resource(EmploymentPosition,
                     '/employment_position',
                     '/employment_position/<int:_id>')
    api.add_resource(ActivateEmploymentPosition,
                     '/activate_employment_position/<int:_id>')
    api.add_resource(EmploymentPositions,
                     '/employment_positions')

    api.add_resource(Shift,
                     '/shift',
                     '/shift/<int:_id>')
    api.add_resource(ActivateShift,
                     '/activate_shift/<int:_id>')
    api.add_resource(Shifts,
                     '/shifts')

    api.add_resource(Employee,
                     '/employee',
                     '/employee/<int:_id>')
    api.add_resource(ActivateEmployee,
                     '/activate_employee/<int:_id>')
    api.add_resource(Employees,
                     '/employees')

    api.add_resource(EmergencyContact,
                     '/emergency_contact',
                     '/emergency_contact/<int:_id>')
    api.add_resource(EmergencyContacts,
                     '/emergency_contacts/<int:_id>')

    api.add_resource(HealthPermit,
                     '/health_permit',
                     '/health_permit/<int:_id>')
    api.add_resource(HealthPermits,
                     '/health_permits/<int:_id>')

    api.add_resource(Countries,
                     '/countries')

    api.add_resource(Passport,
                     '/passport',
                     '/passport/<int:_id>')
    api.add_resource(Passports,
                     '/passports/<int:_id>')

    api.add_resource(UniformItem,
                     '/uniform_item',
                     '/uniform_item/<int:_id>')
    api.add_resource(UniformItems,
                     '/uniform_items')

    api.add_resource(UniformSize,
                     '/uniform_size',
                     '/uniform_size/<int:_id>')
    api.add_resource(UniformSizes,
                     '/uniform_sizes/<int:_id>')

    api.add_resource(UniformRequirement,
                     '/uniform_requirement',
                     '/uniform_requirement/<int:_id>')
    api.add_resource(UniformRequirements,
                     '/uniform_requirements/<int:_id>')

    api.add_resource(Banks,
                     '/banks')

    api.add_resource(BankAccount,
                     '/bank_account',
                     '/bank_account/<int:_id>')
    api.add_resource(ActivateBankAccount,
                     '/activate_bank_account/<int:_id>')
    api.add_resource(BankAccounts,
                     '/bank_accounts/<int:_id>')

    api.add_resource(FamilyRelations,
                     '/family_relations')

    api.add_resource(Dependent,
                     '/dependent',
                     '/dependent/<int:_id>')
    api.add_resource(Dependents,
                     '/dependents/<int:_id>')

    api.add_resource(Schedule,
                     '/schedule',
                     '/schedule/<int:_id>')
    api.add_resource(Schedules,
                     '/schedules/<int:_id>')

    api.add_resource(ScheduleDetail,
                     '/schedule_detail',
                     '/schedule_detail/<int:_id>')
    api.add_resource(ScheduleDetails,
                     '/schedule_details/<int:_id>')

    api.add_resource(Payment,
                     '/payment',
                     '/payment/<int:_id>')
    api.add_resource(Payments,
                     '/payments/<int:_id>')

    api.add_resource(PaymentDetail,
                     '/payment_detail',
                     '/payment_detail/<int:_id>')
    api.add_resource(PaymentDetails,
                     '/payment_details/<int:_id>')

    api.add_resource(Creditor,
                     '/creditor',
                     '/creditor/<int:_id>')
    api.add_resource(ActivateCreditor,
                     '/activate_creditor/<int:_id>')
    api.add_resource(Creditors,
                     '/creditors')

    api.add_resource(Deduction,
                     '/deduction',
                     '/deduction/<int:_id>')
    api.add_resource(ActivateDeduction,
                     '/activate_deduction/<int:_id>')
    api.add_resource(Deductions,
                     '/deductions/<int:_id>')

    api.add_resource(DeductionDetail,
                     '/deduction_detail',
                     '/deduction_detail/<int:_id>')
    api.add_resource(DeductionDetails,
                     '/deduction_details/<int:_id>')
    api.add_resource(Attendance,
                     '/attendance',
                     '/attendance/<int:_id>')
    api.add_resource(Attendances,
                     '/attendances/<int:_id>')

    return app
