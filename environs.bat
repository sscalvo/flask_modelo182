set FLASK_APP=entrypoint.py
REM set FLASK_ENV=development
REM set APP_SETTINGS_MODULE=config.local
set FLASK_ENV=production
set APP_SETTINGS_MODULE=config.prod
flask run