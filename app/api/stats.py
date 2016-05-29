#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Stop, Route, Trip, Agency
from . import api
from sqlalchemy import func


@api.route('/stats')
def get_stats():
    result = db.session.query(func.min(Stop.stop_lat) \
        ,func.min(Stop.stop_lon),func.max(Stop.stop_lat),func.max(Stop.stop_lon),func.count()).first()
    stops = {
        'minLat': result[0],
        'minLon': result[1],
        'maxLat':result[2],
        'maxLon' :result[3],
        'count':result[4]
        }

    routes_count = db.session.query(Route).count()
    trips_count = db.session.query(Trip).count()
    agency_count = db.session.query(Agency).count()
    return jsonify({
        "agencies": {"count": agency_count},
        "stops": stops,
        "routes": {"count": routes_count},
        "trips": {"count": trips_count}
        })
