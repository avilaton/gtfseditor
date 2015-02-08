#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Stop
from . import api
import app.services.geojson as geojson


@api.route('/stops')
@api.route('/stops.<fmt>')
@api.route('/stops/')
def get_stops(fmt="json"):
    bbox = request.args.get('bbox')
    limit = request.args.get('limit')

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
          Stop.stop_lon < east, Stop.stop_lon > west).limit(limit).all()
    else:
        stops = Stop.query.limit(limit).all()

    return jsonify({
        'stops': [stop.to_json for stop in stops]
    })

@api.route('/stops/<id>')
@api.route('/stops/<id>.json')
def get_stop(id):
    item = Stop.query.get_or_404(id)
    return jsonify(item.to_json)

@api.route('/stops/<stop_id>', methods=['DELETE'])
def deleteStop(stop_id):
	stop = Stop.query.filter_by(stop_id = stop_id).one()
	db.session.delete(stop)
	db.session.commit()
	return jsonify({'status': 'success'}), 200

@api.route('/stops/<stop_id>',methods=['PUT', 'OPTIONS'])
def updateStop(stop_id):
  data = request.json
  item = Stop.query.get_or_404(data.get('stop_id'))
  item = Stop(**data)
  db.session.merge(item)
  return jsonify(item.to_json)

@api.route('/stops/', methods=['POST'])
def add_stop():
    item = Stop(**request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json), 201, \
        {'Location': url_for('api.get_stop', id=item.stop_id, _external=True)}
