from flask import Blueprint
from flask.ext.login import login_required

api = Blueprint('api', __name__)


@api.before_request
@login_required
def before_request():
	return

from . import routes
from . import trips
from . import shapes
from . import stops
from . import calendar_dates
from . import calendars
from . import agency
from . import feed
from . import stats
from . import tasks
