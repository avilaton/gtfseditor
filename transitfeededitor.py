#!/usr/bin/env python

import bottle
from bottle import route, static_file, get, post, put, request

import ormgeneric as o
import gtfsdb

db = o.dbInterface('dbRecorridos.sqlite')
tb = gtfsdb.toolbox(db)

@route('/')
def index():
  return static_file('index.html',root='./')

@route('/assets/<filepath:path>')
def server_files(filepath):
  return static_file(filepath, root='./assets/')

@route('/api/stop/<stop_id>')
def findStop(stop_id):
  return tb.findStop(stop_id)

@route('/api/routes/')
@route('/api/routes')
def routes():
  return tb.routes()

@route('/api/route/<route_id>/trips')
@route('/api/route/<route_id>/trips/')
def routeTrips(route_id):
  return tb.trips(route_id)

@route('/api/shape/<shape_id>')
def shape(shape_id):
  return tb.shape(shape_id)

@put('/api/shape/<shape_id>')
def shape(shape_id):
  geojsonShape = request.json
  return tb.saveShape(shape_id, geojsonShape)

@route('/api/trip/<trip_id>/stops')
def tripStops(trip_id):
  return tb.tripStops(trip_id)

@put('/api/trip/<trip_id>/stops')
def saveTripStops(trip_id):
  if 'q' in request.query:
    if request.query['q'] == 'sort':
      result = tb.sortTripStops(trip_id)
    elif request.query['q'] == 'align':
      result = tb.alignTripStops(trip_id)
  else:
    geojsonTrip = request.json  
    result = tb.saveTripStops(trip_id, geojsonTrip)
  return result

@get('/api/trip/<trip_id>/stop/<stop_id>/timepoint')
def is_timepoint(trip_id,stop_id):
  state = db.select('stop_seq', trip_id=trip_id,stop_id=stop_id)[0]
  return {'is_timepoint': state['is_timepoint']}

@put('/api/trip/<trip_id>/stop/<stop_id>/timepoint')
def set_timepoint(trip_id,stop_id):
  is_timepoint = request.params.is_timepoint
  return tb.set_timepoint(trip_id, stop_id, is_timepoint)

@route('/api/bbox')
def getBBOX():
  bbox = request.query['bbox']
  return tb.bbox(bbox)

bottle.debug(True)
app = bottle.app()

if __name__ == '__main__':
  from bottle import run
  run(app,reloader=True)