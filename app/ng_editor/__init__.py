from flask import Blueprint

ng_editor = Blueprint('ng_editor', __name__, static_folder='static/dist', static_url_path='')

from . import views
