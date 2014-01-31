#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEBUG = False

from bottle import route, static_file, get, post, put, delete, request, redirect, hook, response

import database
import gtfsdb
from cork import Cork

# heroku setup
# import urlparse
# import os
# urlparse.uses_netloc.append('postgres')
# url = urlparse.urlparse(os.environ['DATABASE_URL'])
# db = database.Postgress(
#   database = url.path[1:], 
#   user = url.username, 
#   password = url.password, 
#   host = url.hostname,
#   port = url.port
# )

# db = database.Postgress(
#   database='testdb', 
#   user='tester', 
#   password='tester', 
#   host='127.0.0.1'
# )

# db = database.dbInterface('database/dbRecorridos.sqlite')
db = database.dbInterface('database/cba-1.0.0.sqlite')

tb = gtfsdb.toolbox(db)

@hook('after_request')
def after_request():
  pass
  # print("commit to db...")
  # db.connection.commit()

@hook('before_request')
def before_request():
  #db.open()
  return

###############################
# GTFS API
# ========
###############################

@route('/api/reports/unnamed')
def unnamed():
  response.content_type = 'text/plain'
  unnamed = tb.unnamedStops()
  result = 'There are '+str(len(unnamed))+' unnamed stops.\n'
  result += '\n'.join(unnamed)
  return result

@route('/api/reports/available')
def unnamed():
  response.content_type = 'text/plain'
  available = tb.availableStopIds()
  result = 'There are '+str(len(available))+' available stops ids.\n'
  result += '\n'.join(map(str,available))
  return result

###############################
# stops
@route('/api/stop/<stop_id>')
def findStop(stop_id):
  return tb.findStop(stop_id)

@post('/api/stop/<stop_id>')
def createStop(stop_id):
  return tb.createStop(stop_id, request.json)

@put('/api/stop/<stop_id>')
def updateStop(stop_id):
  return tb.updateStop(stop_id, request.json)

@delete('/api/stop/<stop_id>')
def deleteStop(stop_id):
  return tb.deleteStop(stop_id)

@route('/api/bbox')
def getBBOX():
  bbox = request.query['bbox']
  filterQuery = request.query['filter']
  return tb.bbox(bbox, filterQuery)

###############################
# routes
@route('/api/routes/')
@route('/api/routes')
def routes():
  return tb.routes()

@route('/api/route/<route_id>/trips')
@route('/api/route/<route_id>/trips/')
def routeTrips(route_id):
  return tb.trips(route_id)

###############################
# shapes
@route('/api/shape/<shape_id>')
def shape(shape_id):
  return tb.shape(shape_id)

@put('/api/shape/<shape_id>')
def shape(shape_id):
  geojsonShape = request.json
  return tb.saveShape(shape_id, geojsonShape)


###############################
# trips
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
def is_timepoint(trip_id, stop_id):
  trip_stop = tb.getTripStop(trip_id, stop_id)
  return {'is_timepoint': trip_stop['is_timepoint']}

@put('/api/trip/<trip_id>/stop/<stop_id>/timepoint')
def set_timepoint(trip_id,stop_id):
  is_timepoint = request.params.is_timepoint
  return tb.set_timepoint(trip_id, stop_id, is_timepoint)

###############################
# frontend routes
@route('/assets/<filepath:path>')
def server_files(filepath):
  return static_file(filepath, root='./assets/')

@route('/bower_components/<filepath:path>')
def server_files(filepath):
  return static_file(filepath, root='./bower_components/')

@route('/<filepath:path>')
def server_files(filepath):
  return static_file(filepath, root='./public/')

@route('/')
def index():
  return static_file('index.html', root='./public/')

@post('/login')
def login():
  print request.params.email
  print request.params.password
  print request.params.keep

  return

import bottle

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024

if DEBUG == True:
  bottle.debug(True)

app = bottle.app()

if __name__ == '__main__':
  app.run(server='cgi')
  #from bottle import run
  #run(app,reloader=True)