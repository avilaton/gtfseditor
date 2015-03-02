#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import redirect,g, abort, url_for, current_app,render_template
from .. import db, admin
from . import home
from ..models import Agency
from ..models import Calendar
from ..models import Route
from ..models import Trip
from ..models import TripStartTime
from ..models import Stop
from ..models import StopSeq
from ..services.stop_times import StopTimesFactory


@home.route('/')
def index():
	agencies = Agency.query.all()
	routes = Route.query.order_by(Route.route_id).all()
	return render_template('home/index.html', agencies=agencies, routes=routes)

@home.route('/agency/<agency_id>')
def get_agency(agency_id):
	agency = Agency.query.get_or_404(agency_id)
	routes = Route.query.filter(Route.agency_id == agency_id).order_by(Route.route_id).all()
	return render_template('home/agency.html', agency=agency, routes=routes)

@home.route('/routes/<route_id>')
def get_route(route_id):
	route = Route.query.get_or_404(route_id)
	trips = Trip.query.filter(Trip.route_id == route_id)\
        .order_by(Trip.trip_headsign).all()
	return render_template('home/route.html', route=route, trips=trips)

@home.route('/stops/<stop_id>')
def get_stop(stop_id):
	stop = Stop.query.get_or_404(stop_id)
	return render_template('home/stop.html', stop=stop)

@home.route('/routes/<route_id>/trips/<trip_id>')
def get_trip(route_id, trip_id):
	trip = Trip.query.get_or_404(trip_id)
	route = Route.query.get_or_404(route_id)

	used_services = db.session.query(TripStartTime.service_id)\
		.filter_by(trip_id=trip_id).distinct().subquery()

	services = Calendar.query.filter(Calendar.service_id.in_(used_services)).all()

	return render_template('home/trip/index.html', trip=trip, route=route,\
		services=services)

@home.route('/routes/<route_id>/trips/<trip_id>/services/<service_id>')
def get_trip_stops(route_id, trip_id, service_id):
	trip = Trip.query.get_or_404(trip_id)
	route = Route.query.get_or_404(route_id)
	service = Calendar.query.get_or_404(service_id)

	stops = db.session.query(Stop, StopSeq)\
		.join(StopSeq, Stop.stop_id == StopSeq.stop_id)\
		.filter(StopSeq.trip_id == trip_id)\
		.order_by(StopSeq.stop_sequence).all()

	stop_sequence = StopSeq.query.filter(StopSeq.trip_id == trip_id)\
		.order_by(StopSeq.stop_sequence).all()

	trip_start_times = TripStartTime.query\
		.filter_by(trip_id=trip_id, service_id=service_id).all()

	trip_times = []
	for startTimeRow in trip_start_times:
		times = []

		for stop_time in StopTimesFactory.offsetStartTimes(trip_id, stop_sequence, startTimeRow):
			times.append(stop_time['arrival_time'])

		trip_times.append(times)


	time_table = zip(stops, *trip_times)

	return render_template('home/trip/services.html', trip=trip, stops=stops,\
		trip_start_times=trip_start_times, time_table=time_table, route=route,\
		service=service)

