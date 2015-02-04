#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, redirect,g, abort, url_for, current_app,render_template
from .. import db, admin
from ..email import send_email
from ..models import Route, Trip
from . import reports

@reports.route('/')
def index():
	return render_template('reports/index.html')

@reports.route('/routes')
def get_report_routes():
	
	result = db.session.query(Route, Trip).outerjoin(Trip, Route.route_id == Trip.route_id).order_by(Route.route_id).all()

	last = None
	active = 0
	routes = []
	for route, trip in result:
		if getattr(trip, "active", False):
			active += 1
		if last and route.route_id is last:
			routes[-1].get("trips").append(trip.to_json)
		else:
			route_d = route.to_json
			route_d.setdefault("trips", [])
			if trip:
				route_d.get("trips").append(trip.to_json)
			routes.append(route_d)
			last = route.route_id

	return render_template('reports/routes.html', routes=routes, count=len(result), active=active)

@reports.route('/email')
def sendEmail():
	send_email()
	return redirect(url_for('admin.root'))