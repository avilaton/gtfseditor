from flask import Blueprint

admin = Blueprint('admin', __name__, static_folder='client/dist', static_url_path='')

from . import views