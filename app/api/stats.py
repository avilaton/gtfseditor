#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Stop
from . import api
from sqlalchemy import func 


@api.route('/stats')
def get_stats():
	result = db.session.query(func.min(Stop.stop_lat) \
		,func.min(Stop.stop_lon),func.max(Stop.stop_lat),func.max(Stop.stop_lon),func.count()).first()
	data = {'minLat': result[0], 'minLon': result[1], 'maxLat':result[2],'maxLon' :result[3],'numbers':result[4]}
    
	return jsonify(stops=data)