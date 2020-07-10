from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import src.modelo182

app = Flask(__name__)

@app.route('/upload')
def render_uploader():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      #f.save(secure_filename(f.filename))
      f0 = request.files['year0']
      f1 = request.files['year1']
      f2 = request.files['year2']
      f0.save("datos.csv")
      f1.save("year1.txt")
      f2.save("year2.txt")
      
      ejercicio = request.form['ejercicio']

      a = saluda()
      
      return ejercicio + 'files uploaded successfully ' + a
		
if __name__ == '__main__':
   app.run(debug = True)
   
