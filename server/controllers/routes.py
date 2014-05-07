#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route
from server.models import Route

@route('/api/routes/')
@route('/api/routes')
def routes():
  return Route.all()

@route('/api/route/<route_id>/trips')
@route('/api/route/<route_id>/trips/')
def routeTrips(route_id):
  return Route.trips(route_id)
