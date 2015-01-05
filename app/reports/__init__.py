from flask import Blueprint

api = Blueprint('reports', __name__)

from . import views