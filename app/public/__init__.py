# sscalvo@gmail.com
# 05/08/2020

from flask import Blueprint

public_bp = Blueprint('public', __name__, static_folder='downloads', template_folder='templates')

from . import routes
