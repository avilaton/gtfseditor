from flask import Blueprint

trips_bp = Blueprint('trips', __name__, template_folder='templates')

from . import views