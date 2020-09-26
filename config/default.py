# config/default.py
from os.path import abspath, dirname
import os
from flask.helpers import get_root_path

# Define the application directory
BASE_DIR           = dirname(dirname(abspath(__file__)))
DIR_STATIC         = os.path.join(get_root_path('app.public'), 'static' ) 
DIR_DOWNLOADS      = os.path.join(get_root_path('app.public'), 'downloads' ) 

SECRET_KEY         = 'fnskdfji498334ji34jkj43jk5j43jk54j35kj234h5kj3h45jnfjknsdjkcal'
ALLOWED_EXTENSIONS = ['txt', 'csv', 'tsv']
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # max file-upload size= 16 Mb


#MAIL
MAIL_SERVER            = 'smtp.gmail.com'
MAIL_PORT              = 587
MAIL_USE_TLS           = True
MAIL_USERNAME          = "fakemail@gmail.com" 
MAIL_USE_SSL           = False
MAIL_PASSWORD          = "fakepass"
MAIL_DEFAULT_SENDER    = 'appmodelo182@gmail.com'
MAIL_SUPRESS_SEND      = False
MAIL_MAX_EMAILS        = None
MAIL_ASCII_ATTACHMENTS = False



SEND_TO_ADDRESS        = 'sscalvo@gmail.com'
AUTHOR_STR             = 'sscalvo' #einasai
AUTHOR_WEB             = 'http://www.sscalvo.com'
# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''