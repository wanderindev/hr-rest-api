# Set config for development.
DEBUG = True
TESTING = False
SQLALCHEMY_DATABASE_URI = 'postgresql://hr_user:pass@db:5432/hr_dev'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'TmsDxTm53ViWecv9k6sCNuwS'
CLOCK_SECRETS = {
    'abc12345': 'TmsDxTm53ViWecv9k6sCNuwS'
}