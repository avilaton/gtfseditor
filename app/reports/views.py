#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import redirect
from flask import url_for
from flask import render_template

from sqlalchemy import not_

from .. import db, admin
from ..email import send_email
from ..models import Route
from ..models import Trip
from ..models import TripStartTime
from . import reports

@reports.route('/')
def index():
	return render_template('reports/index.html')

@reports.route('/routes')
@reports.route('/routes.html')
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


@reports.route('/times-missing')
@reports.route('/times-missing-active.html')
def get_report_missing_times_active():
	tripStartTimes = db.session.query(TripStartTime.trip_id).distinct().subquery()
	results = db.session.query(Trip, Route.route_short_name).join(Route).\
		filter(not_(Trip.trip_id.in_(tripStartTimes)), Trip.active).\
		order_by(Route.route_short_name, Trip.card_code).all()

	return render_template('reports/times-missing.html', results=results)


@reports.route('/times-missing')
@reports.route('/times-missing.html')
def get_report_missing_times():
	tripStartTimes = db.session.query(TripStartTime.trip_id).distinct().subquery()
	results = db.session.query(Trip, Route.route_short_name).join(Route).\
		filter(not_(Trip.trip_id.in_(tripStartTimes))).\
		order_by(Route.route_short_name, Trip.card_code).all()

	return render_template('reports/times-missing.html', results=results)


@reports.route('/email')
def sendEmail():
	send_email()
	return redirect(url_for('admin.root'))