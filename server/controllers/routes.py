#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request
from bottle import template
import json
from server.models import Route
from server.models import Trip
from server import app

@app.get('/api/routes')
@app.get('/api/routes/')
def routes(db):
  result = db.query(Route, Trip).\
    outerjoin(Trip, Route.route_id == Trip.route_id).\
    order_by(Route.route_id).all()

  last = None
  routes = []
  for route, trip in result:
    if last and route.route_id is last:
      routes[-1].get("trips").append(trip.as_dict)
    else:
      route_d = route.as_dict
      route_d.setdefault("trips", [])
      if trip:
        route_d.get("trips").append(trip.as_dict)
      routes.append(route_d)
      last = route.route_id

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