from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

def handle_upload_files(folder, files):
    paths = []
    for file in files.getlist('year'):
        path = os.path.join(folder, secure_filename(file.filename))
        file.save(path)
        paths.append(path)
    return paths