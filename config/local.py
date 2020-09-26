# config/local.py
from .default import *
APP_ENV = APP_ENV_LOCAL
DEBUG = True
TEMPLATES_AUTO_RELOAD = True #para no tener que reiniciar el servidor cuando cambiamos una template
MAIL_DEBUG_LEVEL       = 5 # Mail verbosity high
