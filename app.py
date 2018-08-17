from flask import Flask, make_response
from flask_jwt import JWT
from flask_restful import Api

from config import config
from resources.absence_authorization import AbsenceAuthorization, \
    AbsenceAuthorizations
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
from resources.raw_attendance import RawAttendance, RawAttendances
from resources.schedule import Schedule, Schedules
from resources.schedule_detail import ScheduleDetail, ScheduleDetails
from resources.sick_note import SickNote, SickNotes
from resources.shift import ActivateShift, Shift, Shifts
from resources.uniform_item import UniformItem, UniformItems
from resources.uniform_requirement import UniformRequirement, \
    UniformRequirements
from resources.uniform_size import UniformSize, UniformSizes
from resources.user import ActivateUser, User, Users
from security import authenticate, identity


# noinspection PyTypeChecker
def create_app(config_name):
    """
    App factory for the creation of a Flask app.

    :param config_name: The key for the config setting to use
    :type config_name: str
    :return: A Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Register the extensions.
    JWT(app, authenticate, identity)
    api = Api(app)

    # Create custom representation for application/text requests.
    @api.representation('application/text')
    def output_text(data, code, headers=None):
        resp = make_response(data, code, headers)
        return resp

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

    api.add_resource(RawAttendance,
                     '/raw_attendance')
    api.add_resource(RawAttendances,
                     '/raw_attendances')

    api.add_resource(SickNote,
                     '/sick_note',
                     '/sick_note/<int:_id>')
    api.add_resource(SickNotes,
                     '/sick_notes/<int:_id>')

    api.add_resource(AbsenceAuthorization,
                     '/absence_authorization',
                     '/absence_authorization/<int:_id>')
    api.add_resource(AbsenceAuthorizations,
                     '/absence_authorizations/<int:_id>')

    return app
