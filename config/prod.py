# config/prod.py
from .default import *
APP_ENV = APP_ENV_PRODUCTION
DEBUG = False
TEMPLATES_AUTO_RELOAD = False #para no tener que reiniciar el servidor cuando cambiamos una template
DIR_UPLOAD         = 'uploads' # besides to app dir
MAIL_DEBUG_LEVEL   = 0 # Mail verbosity 0
print("################# PROD ################")