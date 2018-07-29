# Set config for testing.
DEBUG = False
TESTING = True
SQLALCHEMY_DATABASE_URI = 'postgresql://hr_user:pass@localhost:5432/hr_test'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'TmsDxTm53ViWecv9k6sCNuwS'
CLOCK_SECRETS = {
    'abc12345': 'TmsDxTm53ViWecv9k6sCNuwS'
}
