# sscalvo@gmail.com
# 05/08/2020
from flask import Flask, render_template, request, current_app, flash, session, request
from werkzeug.utils import secure_filename
import os, random, string
import csv
from threading import Thread
import time
    
def allowed_file(filename):
    ALLOWED_EXTENSIONS = current_app.config["ALLOWED_EXTENSIONS"]
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Receives a client-provided filename and returns 
# a  path in the shape: DIR_UPLOAD + uid_filename´random´ + ORIGINAL_EXTENSION
# @path: ruta actual donde se encuentra el fichero subido
# @uid: valor unico aleatoreo del identificador de usuario 
# @cad: string que se acopla a la ruta
def randomize_path(path, uid, cad):
    filename, file_extension = os.path.splitext(path)
    print(path)
    save_path = os.path.join(current_app.config['DIR_UPLOAD'], uid + cad + file_extension)
    return save_path

def handle_upload_files(form):
    fileList = form.fileFieldNames
    file0 = request.files[fileList[0]] # file0 es obligatorio
    file1 = request.files[fileList[1]] # file1 es opcional
    file2 = request.files[fileList[2]] # file2 es opcional
    session["original_filenames"] = "<br>CSV: <span style='color:grey'>" + file0.filename.rstrip() + "</span><br>Exportacion1:<span style='color:grey'> " + file1.filename.rstrip() + "</span><br>Exportacion2: <span style='color:grey'>" + file2.filename.rstrip() + "</span>"
    
    paths = []
    uid = session['user_id']
    incluir_recurrencias = False # Solo si el usuario envia file1 && file2

    if file0.filename == '': # Form-validators should make this option impossible..Just in case
        flash('No selected file')
        return redirect(request.url)
        
    # file0 es obligatorio
    if file0 and allowed_file(file0.filename):
        filename0 = secure_filename(file0.filename)
        paths.append(randomize_path(filename0, uid, '0'))
        file0.save(paths[0])
    
    # ficheros opcionales (necesitamos ambos o ninguno )
    if file1 and file2 and allowed_file(file1.filename) and allowed_file(file2.filename):
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        paths.append(randomize_path(filename1, uid, '1'))
        paths.append(randomize_path(filename2, uid, '2'))
        file1.save(paths[1])
        file2.save(paths[2])
        incluir_recurrencias = True
    else:
        flash('No se ha calculado los donantes recurrentes ya que no has subido los ficheros de los dos años anteriores', 'info')
        
    return (incluir_recurrencias, paths)

    
# https://stackoverflow.com/questions/23917074/javascript-flooring-number-to-order-of-magnitude
def order10(n):
    order = math.floor(math.log(n) / 2.302585092 + 0.000000001)
    return math.pow(10, order)
    

def plot_logarithmic(max, min):
    return (order10(max) / order10(min)) > 1
    
# Generador de random string (para user_id, filenames, etc), ej: '2UR3GT'
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    
# Detectar si un csv tiene 'headers' o no
def sniff(filepath):
   with open(filepath, 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(2048))
        delimiter = repr(dialect.delimiter)
        has_header = False
        csvfile.seek(0)
        if csv.Sniffer().has_header(csvfile.read(2048)):
            has_header = True
        csvfile.close()
        return (delimiter, has_header)

def mail_report():
    html = "La ip " + request.remote_addr + " ha generado un <b>modelo182.</b> " 
    html += "<br><b>NIF del declarante:</b> " +  session.get('params')['NIF_DECLARANTE']
    html += "<br><b>Nombres de los ficheros subidos:</b> " +  session.get('original_filenames')
    html += "<br><br><b>Nombres de los ficheros creados:</b><br> " +  "<br>".join(session.get('paths'))
    return html
    
# Delete all files associated with this client, with given delay in seconds
def _delete_async_delayed(app, files, delay):
    time.sleep(delay)
    # print("Borrando ficheros " + files[0])
    for f in files:
        os.remove(f)
        # print(f, " borrado!")

def delete_files(files, delay=15):
    Thread(target=_delete_async_delayed, args=(current_app._get_current_object(), files, delay)).start()
   