import json
import os

from datetime import timedelta


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TmsDxTm53ViWecv9k6sCNuwS'
    CLOCK_SECRETS = json.loads(os.environ.get('CLOCK_SECRETS')) \
        if os.environ.get('CLOCK_SECRETS') else {
        'abc12345': 'TmsDxTm53ViWecv9k6sCNuwS'
    }
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or \
        'postgresql://hr_user:pass@db:5432/hr_dev'
    TESTING = os.environ.get('TESTING') or False
    DEBUG = os.environ.get('DEBUG') or True
    JWT_EXPIRATION_DELTA = timedelta(seconds=1800)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://hr_user:pass@db:5432/hr_dev'


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://hr_user:pass@' \
                              'localhost:5432/hr_test'


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
