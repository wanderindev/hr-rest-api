from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.department import ActivateDepartment, Department
from resources.marital_status import MaritalStatusList
from resources.organization import ActivateOrganization, Organization, \
    OrganizationList
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
                     '/department/<string:department_name>'
                     '/<int:organization_id>')
    api.add_resource(ActivateDepartment,
                     '/activate_department/<string:department_name>'
                     '/<int:organization_id>')
    api.add_resource(MaritalStatusList,
                     '/marital_statuses')

    return app
