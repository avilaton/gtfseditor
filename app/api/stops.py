#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Stop
from . import api
import app.services.geojson as geojson


@api.route('/stops/')
def get_stops():
    stops = Stop.query.all()
    return jsonify({
        'stops': [item.to_json for item in stops]
    })

@api.route('/stops/<id>')
def get_stop(id):
    item = Stop.query.get_or_404(id)
    return jsonify(item.to_json)

@api.route('/bbox', methods=['GET', 'OPTIONS'])
def getBBOX():
  bounds = request.args.get('bbox')
  w,s,e,n = map(float,bounds.split(','))
  stops = db.session.query(Stop).filter(Stop.stop_lat < n, Stop.stop_lat >s,
   Stop.stop_lon < e, Stop.stop_lon > w).limit(300).all()
  features = []
  for stop in stops:
    ft = geojson.feature(id = stop.stop_id, feature_type = "Point",
      coords = [float(stop.stop_lon), float(stop.stop_lat)],
      properties = stop.to_json)
    features.append(ft)
  return jsonify(geojson.featureCollection(features))

@api.route('/stops/<stop_id>', methods=['DELETE'])
def deleteStop(stop_id):
	stop = Stop.query.filter_by(stop_id = stop_id).one()
	db.session.delete(stop)
	db.session.commit()
	return jsonify({'status': 'success'}), 200

@api.route('/stops/<stop_id>',methods=['PUT', 'OPTIONS'])
def updateStop(stop_id):
  data = request.json
  # """ Stub - should carry out a full update, only updates stop_calle"""
  p = {'stop_id': stop_id}
  p['stop_calle'] = data['properties']['stop_calle'].encode('utf-8')
  p['stop_lon'] = data['geometry']['coordinates'][0]
  p['stop_lat'] = data['geometry']['coordinates'][1]
  # result = self.db.query("""UPDATE stops 
  #   SET stop_calle='{stop_calle}', 
  #     stop_lat='{stop_lat}', stop_lon='{stop_lon}'
  #   WHERE stop_id='{stop_id}'"""
  #   .format(**p))
  # self.db.connection.commit()
  stop = Stop(**p)
  db.session.merge(stop)
  return {'success': True, 'result': p}

# @api.route('/stops/<stop_id>',methods=['POST', 'OPTIONS'])
# def createStop(stop_id):
#   raise NotImplementedError

@api.route('/stops/', methods=['POST'])
def add_stop():
    item = Stop(**request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json), 201, \
        {'Location': url_for('api.get_stop', id=item.stop_id, _external=True)}
