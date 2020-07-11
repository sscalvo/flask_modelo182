from flask import Flask, render_template, request, Response
from werkzeug.utils import secure_filename
import src.modelo182 as m182
import src.tools as tools
DIR_UPLOADS = "uploads"
DIR_SOURCE  = "src"

app = Flask(__name__)

@app.route('/upload')
def render_uploader():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      paths = tools.handle_files(DIR_UPLOADS, request.files)
      df, dfyear1, dfyear2 = m182.load_files(paths)
      linea1    = m182.reg_tipo1(df)
      dflineas2 = m182.reg_tipo2(DIR_SOURCE, df, dfyear1, dfyear2)
      dfinal    = m182.unir(linea1, dflineas2)
      filename, resultado   = m182.convertir_iso8859(dfinal)
      
      return Response(
        resultado,
        mimetype="text/text",
        headers={"Content-disposition":
                 "attachment; filename=" + filename})
      # return render_template('home.html', html=dfinal.to_html())

		
if __name__ == '__main__':
   app.run(debug = True)



    
    