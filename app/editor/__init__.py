from flask import Blueprint

editor = Blueprint('editor', __name__, static_folder='static/dist',
                    static_url_path='',
                    template_folder='templates')

from . import views