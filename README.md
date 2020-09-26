# flask_modelo182
Aplicación web que recibe un csv con los datos de los donantes y (opcionalmente) los ficheros presentados a Hacienda en los dos años anteriores y devuelve el modelo 182 a presentar este año.
Si se incluyen los ficheros presentados en los dos años anteriores, el modelo 182 generado calculará las correspondientes desgravaciones de los donantes recurrentes.

## Pagina web funcionando:
<a href="http://modelo182.sscalvo.com">modelo182.sscalvo.com</a>

## Instalación en Heroku
Es necesario declarar estas Config Vars en los ajustes de tu aplicacion en <a href="https://dashboard.heroku.com/apps/modelo182/settings">heroku</a>:
```
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
 ```
## Formato del CSV
La aplicación espera un fichero CSV con 5 campos, que se corresponden con el **Documento de Identificacion**, **Apellido**, **Nombre**, **Provincia**, **Cantidad**, **Divisa/Moneda**
El nombre de los campos no importa, pero el orden si.
Este es un ejemplo de fichero CSV de donantes válido:

```
National Id,Family Name,Given Name,Address State,Donation Amount,Currency
49625530V,Julián Del Mazo,Rosalía,Barcelona,200 €,EUR
97019472K,Fiorella Bassa,Lucía,Valencia/València,220 €,EUR
21650883V,Alonso Gamella,Laura,Tarragona,100 €,EUR
62525806F,Sánchez Palmeiro, Juan José,Madrid,120 €,EUR
75021099K,Manuela Onieva,Fiorella,Lisboa,100 €,EUR
73042585J,Urizar Payan,Esperanza,Granada,150 €,EUR
72846067F,Malena Roche,Ariana,Alicante/Alacant,150 €,EUR
02683466X,Baza Vilela,Abigail,Granada,100 €,EUR
99410296H,Lopez Besora,Juan,Noord-Holland,150 €,EUR
40024508T,Blanes Cintas,Christian,Granada,100 €,EUR
43599410N,Quinteros Cava,Alfonso,Madrid,200 €,EUR
86747193W,Solanilla Mesa,Damián,Cádiz,200 €,EUR
```
## Por-hacer:
- Hacer predicción de los campos del CSV para permitir csv de diferentes orígenes 

## Contacto:
<a href="http://sscalvo.com">www.sscalvo.com</a>

sscalvo@gmail.com

