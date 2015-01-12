#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request
from bottle import response
from bottle import template
import json
import csv
import StringIO
from server.models import Route
from server.models import Trip
from server.models import StopSeq
from server import app
from sqlalchemy import func


class DictUnicodeProxy(object):
  def __init__(self, d):
    self.d = d
  def __iter__(self):
    return self.d.__iter__()
  def get(self, item, default=None):
    i = self.d.get(item, default)
    if isinstance(i, unicode):
      return i.encode('utf-8')
    return i


@app.get('/api/routes')
@app.get('/api/routes/')
def routes(db):
  result = db.query(Route).order_by(Route.route_id).all()
  routes = [route.as_dict for route in result]
  return {'routes': routes}

@app.get('/api/routes.html')
def routes(db):
  result = db.query(Route, Trip).\
    outerjoin(Trip, Route.route_id == Trip.route_id).\
    order_by(Route.route_id).all()

  last = None
  active = 0
  routes = []
  for route, trip in result:
    if getattr(trip, "active", False):
      active += 1
    if last and route.route_id is last:
      routes[-1].get("trips").append(trip.as_dict)
    else:
      route_d = route.as_dict
      route_d.setdefault("trips", [])
      if trip:
        route_d.get("trips").append(trip.as_dict)
      routes.append(route_d)
      last = route.route_id


  return template('routes.html', routes=routes, count=len(result), active=active)


@app.get('/api/routes.csv')
def routesCsv(db):
  result = db.query(Route, Trip).\
    outerjoin(Trip, Route.route_id == Trip.route_id).\
    order_by(Route.route_id).all()

  rows = []
  fieldnames = None
  route, trip = result[0]
  fieldnames = list(set(route.as_dict.keys() + trip.as_dict.keys())) + ['length']

  for route, trip in result:
    row = route.as_dict
    row.update(trip.as_dict)
    rows.append(row)

  fout = StringIO.StringIO()
  writer = csv.DictWriter(fout, fieldnames=fieldnames)
  writer.writeheader()

  for row in rows:
    length = db.query(func.max(StopSeq.shape_dist_traveled)).filter_by(trip_id=row['trip_id']).one()
    row.update({'length': length[0]})
    writer.writerow(DictUnicodeProxy(row))

  # response.content_type = 'application/csv'
  response.set_header('Content-Type', 'text/plain')

  # response.set_header('Content-Disposition', 
  #   'attachment; filename="{0}"'.format(feed.filename))
  return fout.getvalue()

@app.get('/api/route/<route_id>/trips')
@app.get('/api/route/<route_id>/trips/')
def routeTrips(db, route_id):
  trips = db.query(Trip).filter(Trip.route_id == route_id).all()
  return {'trips': [trip.as_dict for trip in trips]}

@app.route('/api/routes/<route_id>', method=['OPTIONS', 'PUT'])
def updateRoute(db, route_id):
  data = request.json
  route = Route(**data)
  db.merge(route)
  return route.as_dict

@app.route('/api/routes', method=['OPTIONS', 'POST'])
def createRoute(db):
  data = request.json
  print "####Estoy aca",data
  route = Route(**data)
  db.add(route)
  return route.as_dict

@app.route('/api/routes/<route_id>', method=['OPTIONS', 'DELETE'])
def deleteRoute(db, route_id):
  route = db.query(Route).filter(Route.route_id == route_id).one()
  db.delete(route)
  return {'success': True}