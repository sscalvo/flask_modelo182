# config/default.py
from os.path import abspath, dirname
import os
from flask.helpers import get_root_path

# Define the application directory
BASE_DIR           = dirname(dirname(abspath(__file__)))
DIR_STATIC         = os.path.join(get_root_path('app.public'), 'static' ) 
DIR_DOWNLOADS      = os.path.join(get_root_path('app.public'), 'downloads' ) 

SECRET_KEY         = 'your secret key'
ALLOWED_EXTENSIONS = ['txt', 'csv', 'tsv']
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # max file-upload size= 16 Mb


#MAIL
MAIL_SERVER            = 'smtp.gmail.com'
MAIL_PORT              = 587
MAIL_USE_TLS           = True
MAIL_USERNAME          = "email address from where app will be sendig emails"
MAIL_USE_SSL           = False
MAIL_PASSWORD          = "password for MAIL_USERNAME address"
MAIL_DEFAULT_SENDER    = 'email address shown as sender'
MAIL_SUPRESS_SEND      = False
MAIL_MAX_EMAILS        = None
MAIL_ASCII_ATTACHMENTS = False



SEND_TO_ADDRESS        = 'email address that will receive emails (you may want this to be your own email)'
AUTHOR_STR             = 'sscalvo'
AUTHOR_WEB             = 'http://www.sscalvo.com'
# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''