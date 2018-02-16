from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.country import CountryList
from resources.department import ActivateDepartment, Department
from resources.emergency_contact import EmergencyContact
from resources.employee import ActivateEmployee, Employee
from resources.employment_position import ActivateEmploymentPosition, \
    EmploymentPosition
from resources.health_permit import HealthPermit
from resources.marital_status import MaritalStatusList
from resources.organization import ActivateOrganization, Organization, \
    OrganizationList
from resources.passport import Passport
from resources.shift import ActivateShift, Shift
from resources.user import ActivateUser, User
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
                     '/organization/<string:organization_name>')
    api.add_resource(ActivateOrganization,
                     '/activate_organization/<string:organization_name>')
    api.add_resource(OrganizationList,
                     '/organizations')

    api.add_resource(User,
                     '/user',
                     '/user/<string:username>')
    api.add_resource(ActivateUser,
                     '/activate_user/<string:username>')

    api.add_resource(Department,
                     '/department',
                     '/department/<string:department_name>')
    api.add_resource(ActivateDepartment,
                     '/activate_department/<string:department_name>')

    api.add_resource(MaritalStatusList,
                     '/marital_statuses')

    api.add_resource(EmploymentPosition,
                     '/employment_position',
                     '/employment_position/<string:position_name>')
    api.add_resource(ActivateEmploymentPosition,
                     '/activate_employment_position/<string:position_name>')

    api.add_resource(Shift,
                     '/shift',
                     '/shift/<string:shift_name>')
    api.add_resource(ActivateShift,
                     '/activate_shift/<string:shift_name>')

    api.add_resource(Employee,
                     '/employee',
                     '/employee/<int:employee_id>')
    api.add_resource(ActivateEmployee,
                     '/activate_employee/<int:employee_id>')

    api.add_resource(EmergencyContact,
                     '/emergency_contact',
                     '/emergency_contact/<int:contact_id>')

    api.add_resource(HealthPermit,
                     '/health_permit',
                     '/health_permit/<int:permit_id>')

    api.add_resource(CountryList,
                     '/countries')

    api.add_resource(Passport,
                     '/passport',
                     '/passport/<int:passport_id>')

    return app
