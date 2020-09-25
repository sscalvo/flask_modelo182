# sscalvo@gmail.com
# 05/08/2020
import os
from app import create_app
#app = create_app()
settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)

