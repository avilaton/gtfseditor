#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request, template, abort
import server.geojson as geojson
from server import app
from server.models import Stop

@app.route('/api/stop/<stop_id>')
def index(db, stop_id):
  stop = db.query(Stop).filter(Stop.stop_id == stop_id).first()
  if stop:
    return stop.as_dict
  else:
    abort(404, 'no such stop_id')

@app.route('/api/bbox')
def getBBOX(db):
  bounds = request.query['bbox']
  w,s,e,n = map(float,bounds.split(','))
  print w,s,e,n
  stops = db.query(Stop).filter(Stop.stop_lat < n, Stop.stop_lat >s,
   Stop.stop_lon < e, Stop.stop_lon > w).limit(300).all()
  features = []
  for stop in stops:
    ft = geojson.feature(id = stop.stop_id, feature_type = "Point",
      coords = [float(stop.stop_lon), float(stop.stop_lat)],
      properties = stop.as_dict)
    features.append(ft)
  geojson.featureCollection(features)
  return geojson.featureCollection(features)

@app.delete('/api/stop/<stop_id>')
def deleteStop(db, stop_id):
  result = db.query(Stop).filter(Stop.stop_id == stop_id).delete()
  return {'success': bool(result), 'stop_id': stop_id}

@app.put('/api/stop/<stop_id>')
def updateStop(stop_id):
  raise NotImplementedError

@app.post('/api/stop/<stop_id>')
def createStop(db, stop_id):
  raise NotImplementedError
