#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request
import json
from server.models import Agency
from server.models import Trip
from server import app

@app.get('/api/agency')
@app.get('/api/agency/')
def agency(db):
  agencys = db.query(Agency).order_by(Agency.agency_name).all()
  return {'agency': [agency.as_dict for agency in agencys]}

# @app.get('/api/route/<route_id>/trips')
# @app.get('/api/route/<route_id>/trips/')
# def routeTrips(db, route_id):
#   trips = db.query(Trip).filter(Trip.route_id == route_id).all()
#   return {'trips': [trip.as_dict for trip in trips]}

# @app.route('/api/routes/<route_id>', method=['OPTIONS', 'PUT'])
# def updateRoute(db, route_id):
#   data = request.json
#   route = Route(**data)
#   db.merge(route)
#   return route.as_dict

# @app.route('/api/routes', method=['OPTIONS', 'POST'])
# def createRoute(db):
#   data = request.json
#   print data
#   route = Route(**data)
#   db.add(route)
#   return route.as_dict

# @app.route('/api/routes/<route_id>', method=['OPTIONS', 'DELETE'])
# def deleteRoute(db, route_id):
#   route = db.query(Route).filter(Route.route_id == route_id).one()
#   db.delete(route)
#   return {'success': True}