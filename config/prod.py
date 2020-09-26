# config/prod.py
from .default import *
APP_ENV = APP_ENV_PRODUCTION
DEBUG = False
TEMPLATES_AUTO_RELOAD = False #para no tener que reiniciar el servidor cuando cambiamos una template
DIR_UPLOAD         = 'C:\\tmp_uploads' # HEROKU ??
MAIL_DEBUG_LEVEL   = 0 # Mail verbosity 0