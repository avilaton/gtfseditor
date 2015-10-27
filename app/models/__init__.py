#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy_continuum.plugins import FlaskPlugin
from sqlalchemy_continuum import make_versioned
from flask.globals import _app_ctx_stack, _request_ctx_stack


def fetch_current_user_id():
    from flask.ext.login import current_user

    # Return None if we are outside of request context.
    if _app_ctx_stack.top is None or _request_ctx_stack.top is None:
        return
    try:
        return current_user.user_id
    except AttributeError:
        return

flask_plugin = FlaskPlugin(current_user_id_factory=fetch_current_user_id)


make_versioned(plugins=[flask_plugin])


from app.models.agency import Agency
from app.models.calendar import Calendar
from app.models.calendardate import CalendarDate
from app.models.fareattribute import FareAttribute
from app.models.farerule import FareRule
from app.models.feedinfo import FeedInfo
from app.models.frequency import Frequency
from app.models.permission import Permission
from app.models.role import Role
from app.models.route import Route
from app.models.routefrequency import RouteFrequency
from app.models.shape import Shape
from app.models.shapepath import ShapePath
from app.models.stop import Stop
from app.models.stopseq import StopSeq
from app.models.stoptime import StopTime
from app.models.transfer import Transfer
from app.models.trip import Trip
from app.models.tripstarttime import TripStartTime
from app.models.user import User
