# sscalvo@gmail.com
# 05/08/2020
from flask import current_app, render_template, request, redirect, url_for, flash, session, current_app,send_from_directory
from flask.helpers import get_root_path
from app.common.mail import send_email


from werkzeug.utils import secure_filename
import os
from . import public_bp
from .forms import UploadForm, ContactForm
from .tools import handle_upload_files, id_generator, mail_report, delete_files
from .modelo182 import load_form_fields, load_uploaded_files, load_local_dataframes, reg_tipo1, reg_tipo2, unir
from .modelo182 import convertir_iso8859, save_to_file, get_stats


@public_bp.route('/', methods = ['GET', 'POST'])   
def datos():
    ''' PASO 1: Recoge datos del form, los procesa, genera el mod182 y redirige a column-matching page
    '''
    # flash("Flash for flash", "info")
    if not 'user_id' in session:
        session['user_id'] = id_generator(size=10)
   
    form = UploadForm(meta={'csrf': True})
    if form.validate_on_submit():
        hay_recurrencias, paths     = handle_upload_files(form)
        params                      = load_form_fields(form) # initlizing modelo182   

        session["hay_recurrencias"] = hay_recurrencias
        session["paths"]            = paths
        session["params"]           = params

        ### If future splitting of formulario in several HTTP steps:  ###############
        # ------------------- split here ----------------
        # hay_recurrencias = session["hay_recurrencias"]
        # paths = session["paths"]           
        # params = session["params"]          
        #############################################################
        
        df, dfyear1, dfyear2        = load_uploaded_files(paths, params, hay_recurrencias)
        DIR_STATIC                  = current_app.config["DIR_STATIC"] #provincias.tsv & cautonomas.csv  
        dfprov, dfca                = load_local_dataframes(DIR_STATIC, params)         
        linea1                      = reg_tipo1(df, params)
        ## charts ????????????
        charts                      = [] # ira guardando los charts (como json) para  enviar a Chart.js (result.html)
        dflineas2                   = reg_tipo2(charts, df, dfyear1, dfyear2, dfprov, dfca, params, hay_recurrencias)
        dfinal                      = unir(linea1, dflineas2)
        resultado                   = convertir_iso8859(dfinal)
        DIR_DOWNLOADS               = current_app.config["DIR_DOWNLOADS"]
        print("#####################  DIR_DOWNLOADS = ", DIR_DOWNLOADS, " #########")
        print("#####################  DIR_UPLOADS = ", current_app.config["DIR_UPLOADS"], " #########")
        filename                    = save_to_file(DIR_DOWNLOADS, resultado, params, session['user_id']) # hard-disk write
        stats                       = get_stats()        

        session['file182'] = filename
        session['charts'] = charts

        return redirect(url_for('public.result'))
    if form.is_submitted():
        flash('Has olvidado de rellenar algunos datos. Por favor, revisa de nuevo el formulario, gracias!')
    return render_template("public/input182.html", form=form)
    
    
@public_bp.route('/resultado')
def result():
    filename = session.get('file182')
    if filename != None:
        return render_template('public/output182.html', charts=session['charts'], filename_result=session['file182'] ) #, filename_result=session['file182'], charts=session['charts'])
    else: # Just in case someone refreshes browser
        return redirect(url_for("public.datos"))
      
        
@public_bp.route('/downloads/<filename>')
def download(filename):
    # filename = session.get('file182')
    html = mail_report()
    SEND_TO_ADDRESS = current_app.config["SEND_TO_ADDRESS"]
    MAIL_DEFAULT_SENDER = current_app.config["MAIL_DEFAULT_SENDER"]
    send_email("Modelo182 generado", MAIL_DEFAULT_SENDER, [SEND_TO_ADDRESS], html, html_body=html)
    paths = session['paths'] # The *maybe 3* uploaded files
    DIR_DOWNLOADS = current_app.config["DIR_DOWNLOADS"]
    paths.append(os.path.join(DIR_DOWNLOADS, filename) ) # The generated mod182 file
    delete_files( paths, delay=15 ) # Delete them in 15 seconds
    session.clear() 
    return send_from_directory(DIR_DOWNLOADS, filename, attachment_filename=filename, as_attachment=True)
        
@public_bp.route('/sample')
def sample():
    # session.clear() 
    filename="ejemplo_donantes.csv"
    DIR_DOWNLOADS = current_app.config["DIR_DOWNLOADS"]
    return send_from_directory(DIR_DOWNLOADS, filename, attachment_filename=filename, as_attachment=True)

@public_bp.route('/contacto/', methods = ['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('public/contact.html', form = form)
        else:
            html = """<b>Nombre:</b> %s<br/>
            <b>Email:</b> %s<br/>
            <p style="color:red">%s</p>
            """ % (form.nombre.data, form.email.data, form.mensaje.data)
            SEND_TO_ADDRESS = current_app.config["SEND_TO_ADDRESS"]
            MAIL_DEFAULT_SENDER = current_app.config["MAIL_DEFAULT_SENDER"]
            send_email(form.titulo.data, MAIL_DEFAULT_SENDER, [ SEND_TO_ADDRESS], html, html_body=html)
            return render_template('public/contact.html', success=True)
    elif request.method == 'GET':
        return render_template('public/contact.html', titulo = 'Contactar', form = form)
        
@public_bp.context_processor
def inject_user():
    # variables to inject into templates
    return { 
        'author_str' :  current_app.config["AUTHOR_STR"],
        'author_url' :  current_app.config["AUTHOR_WEB"]
        }
