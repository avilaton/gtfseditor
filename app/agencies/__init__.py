from flask import Blueprint

agencies_bp = Blueprint('agencies', __name__, template_folder='templates')

from . import views