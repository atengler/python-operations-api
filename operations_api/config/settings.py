# Flask settings
FLASK_SERVER_HOST = 'localhost'
FLASK_SERVER_PORT = '8001'
FLASK_DEBUG = True
FLASK_SECRET_KEY = 'secretsecretsecret'

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
# Turn off the Flask-SQLAlchemy event system
SQLALCHEMY_TRACK_MODIFICATIONS = False

try:
    from operations_api.local_settings import *  # noqa
except ImportError:
    pass
