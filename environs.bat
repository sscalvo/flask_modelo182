set FLASK_APP=entrypoint.py
set FLASK_ENV=development REM production
set APP_SETTINGS_MODULE=config.local REM config.prod
set DIR_UPLOADS=C:\tmp_uploads
set SECRET_KEY=8bcbcd3386877c987b8ec6b866af770772241c26818d920dda9b32cb9cb4dffb665def351b48c385
set MAIL_USERNAME=elsepes@gmail.com
set MAIL_PASSWORD=ev1@nd0r
set MAIL_DEFAULT_SENDER=appmodelo182@gmail.com
set SEND_TO_ADDRESS=sscalvo@gmail.com
set AUTHOR_STR=sscalvo
set AUTHOR_WEB=http://www.sscalvo.com
flask run