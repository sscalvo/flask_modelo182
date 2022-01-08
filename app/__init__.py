# sscalvo@gmail.com
# 05/08/2020
from flask import Flask, render_template
from flask_cors import CORS, cross_origin # https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
from flask_mail import Mail
# from flask_talisman import Talisman

mail = Mail() # 2. Instanciamos un objeto de tipo Mail

# https://j2logo.com/tutorial-flask-leccion-8-gestion-manejo-errores-excepciones/
def registrar_error_handlers(app):
    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404


def create_app(settings_module='config.prod'):
    app = Flask(__name__)
    print(f"el Flask(__name__) es {__name__}")
    # Talisman(app)
    app.config.from_object(settings_module)
    mail.init_app(app)  # 3. Inicializamos el objeto mail
    app.extensions['mail'].debug = app.config["MAIL_DEBUG_LEVEL"] # https://stackoverflow.com/questions/58309600/disable-logging-in-flask-mail-when-sending-message
   
    #cors = CORS(app)
    #app.config['CORS_HEADERS'] = 'Content-Type'
    #usar decorador en la vista que genere problemas: @cross_origin()
    
    # Registro de los Blueprints
    from .public import public_bp
    app.register_blueprint(public_bp)
#    from .admin import admin_bp
#    app.register_blueprint(admin_bp)

    # Custom error handlers
    registrar_error_handlers(app)

    return app