#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request
import json
from server.models import Route
from server.models import Trip
from server import app

@app.get('/api/routes')
@app.get('/api/routes/')
def routes(db):
  routes = db.query(Route).order_by(Route.route_short_name).all()
  return {'routes': [route.as_dict for route in routes]}

@app.get('/api/route/<route_id>/trips')
@app.get('/api/route/<route_id>/trips/')
def routeTrips(db, route_id):
  trips = db.query(Trip).filter(Trip.route_id == route_id).all()
  return {'trips': [trip.as_dict for trip in trips]}


@app.post('/api/routes/<route_id>')
def shape(db, route_id):
  data = request.json
  route = Route(**data)
  print route.as_dict
  db.merge(route)
  return 
