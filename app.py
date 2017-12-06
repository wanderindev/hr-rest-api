from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.organization import Organization, OrganizationList
from resources.user import User
from security import authenticate, identity


def create_app(config_type):
    app = Flask(__name__, instance_relative_config=True)

    # Load config settings for development or testing.
    app.config.from_object(f'config.{config_type}')

    # Apply production settings, if available.
    app.config.from_pyfile('settings.py', silent=True)

    # Register the extensions.
    JWT(app, authenticate, identity)
    api = Api(app)

    # Add API resources.
    api.add_resource(Organization, '/organization',
                     '/organization/<string:name>')
    api.add_resource(OrganizationList, '/organizations')
    api.add_resource(User, '/user', '/user/<string:username>')

    return app
