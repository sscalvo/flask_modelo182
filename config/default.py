# config/default.py
from os.path import abspath, dirname
import os
from flask.helpers import get_root_path

# Define the application directory
BASE_DIR           = dirname(dirname(abspath(__file__)))
DIR_STATIC         = os.path.join(get_root_path('app.public'), 'static' ) 
DIR_DOWNLOADS      = os.path.join(get_root_path('app.public'), 'downloads' ) 

SECRET_KEY         = os.environ['SECRET_KEY']
ALLOWED_EXTENSIONS = ['txt', 'csv', 'tsv']
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # max file-upload size= 16 Mb


#MAIL
MAIL_SERVER            = 'smtp.gmail.com'
MAIL_PORT              = 587
MAIL_USE_TLS           = True
MAIL_USERNAME          = os.environ['MAIL_USERNAME']
MAIL_USE_SSL           = False
MAIL_PASSWORD          = os.environ['MAIL_PASSWORD']
MAIL_DEFAULT_SENDER    = os.environ['MAIL_DEFAULT_SENDER']
MAIL_SUPRESS_SEND      = False
MAIL_MAX_EMAILS        = None
MAIL_ASCII_ATTACHMENTS = False


#OWNER
SEND_TO_ADDRESS        = os.environ['SEND_TO_ADDRESS']
AUTHOR_STR             = os.environ['AUTHOR_STR'] # string placed on top navbar
AUTHOR_WEB             = os.environ['AUTHOR_WEB'] # url link for AUTHOR_STR

# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''

print("#################  ", MAIL_USERNAME, " ################")
print("#################  ", MAIL_USERNAME, " ################")