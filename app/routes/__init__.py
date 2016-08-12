from flask import Blueprint

routes_bp = Blueprint('routes', __name__, template_folder='templates')

from . import views