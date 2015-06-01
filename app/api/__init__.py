from flask import Blueprint
from flask import redirect
from flask import request
from flask import url_for
from flask.ext.login import login_required
from flask.ext.login import current_user
from .errors import unauthorized

api = Blueprint('api', __name__)


@api.before_request
def before_request():
	if request.method != 'GET' and not current_user.is_authenticated():
		return unauthorized('user is not authenticated')


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
