#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app
from flask import Response
from flask import json
from .. import db
from ..models import Stop
from ..models import StopSeq
from ..models import Route
from ..models import Trip
from . import api
from .decorators import admin_required


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@api.route('/stops')
@api.route('/stops.<fmt>')
@api.route('/stops/')
def get_stops(fmt="json"):
    bbox = request.args.get('bbox')
    limit = request.args.get('limit')
    filter_stop_code = request.args.get('filter')

    try:
      limit = int(limit)
    except Exception, e:
      limit = 300

    try:
      bounds = True
      west, south, east, north = map(float,bbox.split(','))
    except Exception, e:
      bounds = None

    if bounds:
        stops = Stop.query.filter(Stop.stop_lat < north, Stop.stop_lat > south,
            Stop.stop_lon < east, Stop.stop_lon > west)
    else:
        stops = Stop.query

    if filter_stop_code:
      stops = stops.filter(Stop.stop_code.contains(filter_stop_code)).limit(limit).all()
    else:
      stops = stops.limit(limit).all()

    return Response(json.dumps([i.to_json for i in stops]),
        mimetype='application/json')


@api.route('/stops/<id>')
@api.route('/stops/<id>.json')
def get_stop(id):
    item = Stop.query.get_or_404(id)
    return jsonify(item.to_json)

@api.route('/stops/<stop_id>', methods=['DELETE'])
@admin_required
def deleteStop(stop_id):
	stop = Stop.query.filter_by(stop_id = stop_id).one()
	db.session.delete(stop)
	db.session.commit()
	return jsonify({'status': 'success'}), 200

@api.route('/stops/<stop_id>',methods=['PUT', 'OPTIONS'])
def updateStop(stop_id):
  data = request.json
  item = Stop(**data)
  db.session.merge(item)
  db.session.commit()
  return jsonify(item.to_json)

@api.route('/stops/', methods=['POST'])
@admin_required
def add_stop():
    item = Stop(**request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json), 201, \
        {'Location': url_for('api.get_stop', id=item.stop_id, _external=True)}

@api.route('/stops/<stop_id>/seqs')
@api.route('/stops/<stop_id>/seqs.json')
def get_stop_seqs(stop_id):
    items = db.session.query(Route.route_short_name, Trip.trip_headsign,
        Trip.card_code, Trip.direction_id).\
      join(Trip, Route.route_id==Trip.route_id).\
      join(StopSeq, StopSeq.trip_id == Trip.trip_id).\
      filter(StopSeq.stop_id==stop_id).all()
    body = [{
      'route_id':item[0],
      'trip_headsign':item[1],
      'card_code': item[2],
      'direction_id': item[3]
      } for item in items]

    return Response(json.dumps(body),  mimetype='application/json')
