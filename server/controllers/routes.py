#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, request, post, put, delete
# remove this global latter on
from server.transitfeededitor import tb

@route('/api/routes/')
@route('/api/routes')
def routes():
  return tb.routes()

@route('/api/route/<route_id>/trips')
@route('/api/route/<route_id>/trips/')
def routeTrips(route_id):
  return tb.trips(route_id)
