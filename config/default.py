# config/default.py
from os.path import abspath, dirname
import os
from flask.helpers import get_root_path
# Make sure all the requiered 'os.environ' variables are available at OS level before running the app
# Define the application directory
BASE_DIR           = dirname(dirname(abspath(__file__)))
DIR_STATIC         = os.path.join(get_root_path('app.public'), 'static' ) 
DIR_DOWNLOADS      = os.path.join(get_root_path('app.public'), 'downloads' ) 
DIR_UPLOADS        = os.environ['DIR_UPLOADS'] 

SECRET_KEY         = os.environ['SECRET_KEY']
ALLOWED_EXTENSIONS = ['txt', 'csv', 'tsv']
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # max file-upload size= 16 Mb


#MAIL
MAIL_SERVER            = os.environ['MAIL_SERVER']
MAIL_PORT              = 587
MAIL_USE_TLS           = True
MAIL_USE_SSL           = False
MAIL_USERNAME          = os.environ['MAIL_USERNAME'] # email from which mails will be sent 
MAIL_PASSWORD          = os.environ['MAIL_PASSWORD'] # pssword of MAIL_USERNAME
MAIL_DEFAULT_SENDER    = os.environ['MAIL_DEFAULT_SENDER'] # 'sent from' (not really important)
MAIL_SUPRESS_SEND      = False
MAIL_MAX_EMAILS        = None
MAIL_ASCII_ATTACHMENTS = False

#OWNER
SEND_TO_ADDRESS        = os.environ['SEND_TO_ADDRESS'] # Probably your personal email, to receive app feedback emails
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
print("#################  ", DIR_DOWNLOADS, " ################")
print("#################  ", DIR_UPLOADS, " ################")