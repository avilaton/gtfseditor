from flask import Blueprint

editor = Blueprint('editor', __name__, static_folder='static/dist', static_url_path='')

from . import views