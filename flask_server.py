from flask import Flask, render_template, request, Response, send_file, session
from werkzeug.utils import secure_filename
import src.modelo182 as m182
import src.tools as tools
import io
DIR_UPLOADS = "uploads"
DIR_DOWNLOADS = "downloads"
DIR_LOCAL_FILES = "src\\mod182\\files"

app = Flask(__name__)
app.secret_key = 'Mira, te he llamado pork me kiero comprar un portatil'

@app.route('/upload')
def render_uploader():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      paths = tools.handle_upload_files(DIR_UPLOADS, request.files)
      df, dfyear1, dfyear2 = m182.load_uploaded_files(paths)
      dfprov, dfca = m182.load_local_dataframes(DIR_LOCAL_FILES) #provincias & comunidades autónomas
      linea1    = m182.reg_tipo1(df)
      dflineas2 = m182.reg_tipo2(DIR_DOWNLOADS, df, dfyear1, dfyear2, dfprov, dfca)
      dfinal    = m182.unir(linea1, dflineas2)
      resultado = m182.convertir_iso8859(dfinal)
      filename  = m182.save_to_file(resultado) # hard-disk write
      stats     = m182.get_stats()
      
      # session['fichero'] = filename

      return render_template('stats.html', fichero=filename, stats=stats)

      # return Response(
        # resultado,
        # mimetype="text/text",
        # headers={"Content-disposition":
                 # "attachment; filename=" + filename})



    
if __name__ == '__main__':
   app.run(host='0.0.0.0', debug = True)



    
    