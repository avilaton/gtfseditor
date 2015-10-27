#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import Base
from sqlalchemy import orm

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

from .permission import Permission
from .role import Role
from .user import User

from .gtfs.agency import Agency
from .gtfs.calendar import Calendar
from .gtfs.calendardate import CalendarDate
from .gtfs.fareattribute import FareAttribute
from .gtfs.farerule import FareRule
from .gtfs.feedinfo import FeedInfo
from .gtfs.frequency import Frequency
from .gtfs.route import Route
from .gtfs.routefrequency import RouteFrequency
from .gtfs.shape import Shape
from .gtfs.shapepath import ShapePath
from .gtfs.stop import Stop
from .gtfs.stopseq import StopSeq
from .gtfs.stoptime import StopTime
from .gtfs.transfer import Transfer
from .gtfs.trip import Trip
from .gtfs.tripstarttime import TripStartTime

orm.configure_mappers()


