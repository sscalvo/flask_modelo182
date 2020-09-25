# sscalvo@gmail.com
# 05/08/2020
import os
from app import create_app
#app = create_app()
# settings_module = os.getenv('APP_SETTINGS_MODULE')  #comentada para Heroku
# app = create_app(settings_module)  # comentada para Heroku
app = create_app() # default value for setting_module is 'config.prod'. This way we dont need environ vars in Heroku

