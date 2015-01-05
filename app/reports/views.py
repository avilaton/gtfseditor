#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app,render_template
from .. import db
from ..models import Route, Trip
from . import reports

@reports.route('/routes')
def get_report_routes():
	print "SASAS"
	# print "EEEEEEEEEEE"
 #  	result = db.query(Route, Trip).\
 #    outerjoin(Trip, Route.route_id == Trip.route_id).\
 #    order_by(Route.route_id).all()

 #  last = None
 #  active = 0
 #  routes = []
 #  for route, trip in result:
 #    if getattr(trip, "active", False):
 #      active += 1
 #    if last and route.route_id is last:
 #      routes[-1].get("trips").append(trip.as_dict)
 #    else:
 #      route_d = route.as_dict
 #      route_d.setdefault("trips", [])
 #      if trip:
 #        route_d.get("trips").append(trip.as_dict)
 #      routes.append(route_d)
 #      last = route.route_id


 #  return render_template('routes.html', routes=routes, count=len(result), active=active)