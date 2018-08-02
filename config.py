import json, os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TmsDxTm53ViWecv9k6sCNuwS'
    CLOCK_SECRETS = json.loads(os.environ.get('CLOCK_SECRETS')) \
        if os.environ.get('CLOCK_SECRETS') else {
        'abc12345': 'TmsDxTm53ViWecv9k6sCNuwS'
    }

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
