# flask_modelo182
Aplicación web que recibe un csv con los datos de los donantes y (opcionalmente) los ficheros presentados a Hacienda en los dos años anteriores y devuelve el modelo 182 a presentar este año.

## Pagina web:
<a href="http://modelo182.sscalvo.com">modelo182.sscalvo.com</a>

## Instalación en Heroku
Es necesario declarar estas Config Vars en los ajustes de tu aplicacion en <a href="https://dashboard.heroku.com/apps/modelo182/settings">heroku</a>:

FLASK_APP=entrypoint.py
FLASK_ENV=development
APP_SETTINGS_MODULE=config.local
DIR_UPLOADS=/tmp
SECRET_KEY=45d8dscm2.....secret_key.....86fd0dc333
MAIL_SERVER=mail.server.com
MAIL_USERNAME=<un email>
MAIL_PASSWORD=<un password para el email de arriba>
MAIL_DEFAULT_SENDER=<un email>
SEND_TO_ADDRESS=<direccion de logs>
AUTHOR_STR=<nombre>
AUTHOR_WEB=<url>
  
## TODO:
- Hacer predicción de los campos del CSV para permitir csv de diferentes orígenes 



