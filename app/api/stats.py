#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Stop
from . import api
from sqlalchemy import func 


@api.route('/stats')
def get_stats():
	stops = db.session.query(func.min(Stop.stop_lat) \
		,func.min(Stop.stop_lon),func.max(Stop.stop_lat),func.max(Stop.stop_lon),func.count()).first()
	list = {'minLat': stops[0], 'minLon': stops[1], 'maxLat':stops[2],'maxLon' :stops[3],'numbers':stops[4]}
    
	return jsonify(stops=list)