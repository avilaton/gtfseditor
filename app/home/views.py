#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import groupby
from flask import render_template, make_response
import sqlalchemy as sa
import StringIO
import unicodecsv as csv

from .. import db
from . import home
from ..models import Agency
from ..models import Calendar
from ..models import Route
from ..models import Trip
from ..models import TripStartTime
from ..models import Stop
from ..models import StopSeq
from ..services.stop_times import offset_sequence_times

array_type = sa.dialects.postgresql.ARRAY(sa.types.String, as_tuple=True)


def remove_nulls(items):
	if items:
		return filter(None, items)
	else:
		return tuple()

def get_stops_and_routes():
	distinct_route_names = sa.distinct(Route.route_short_name)
	route_agg_dis_active = sa.func.array_agg(
		distinct_route_names,
		type_=array_type
	).filter(Route.active).label('routes')
	route_agg_dis_inactive = sa.func.array_agg(
		distinct_route_names,
		type_=array_type
	).filter(Route.active.isnot(True)).label('routes_inactive')
	rows = db.session.query(
		Stop,
		route_agg_dis_active,
		route_agg_dis_inactive
	).outerjoin(StopSeq, Trip, Route)
	rows = rows.group_by(Stop.stop_id).order_by(Stop.stop_code)
	rows = ((r.Stop, remove_nulls(r.routes), remove_nulls(r.routes_inactive)) for r in rows)
	return rows


@home.route('/')
def index():
	agency_routes = db.session.query(Agency, Route).join(Route)\
		.order_by(Agency.agency_name, Route.route_short_name).all()
	agencies = groupby(agency_routes, lambda x: x.Agency)
	return render_template('home/index.html', agencies=agencies)

@home.route('/routing')
def routing():
	return render_template('home/routing/index.html')

@home.route('/stops')
def stops():
	rows = get_stops_and_routes()
	return render_template('home/stops/list.html', rows=rows)

@home.route('/stops.<fmt>')
def stops_kml(fmt='csv'):
	rows = get_stops_and_routes()
	if fmt == 'kml':
		content = render_template('stops.kml', rows=rows)
	elif fmt == 'csv':
		si = StringIO.StringIO()
		writer = csv.DictWriter(si, ['stop_code', 'stop_name', 'active_routes', 'inactive_routes'])
		writer.writeheader()
		for stop, active_routes, inactive_routes in rows:
			writer.writerow({
				'stop_code': stop.stop_code,
				'stop_name': stop.stop_name,
				'active_routes': ', '.join(active_routes),
				'inactive_routes': ', '.join(inactive_routes),
				})
		content = si.getvalue()

	response = make_response(content)
	response.headers["Content-Disposition"] = "attachment; filename=stops."+fmt
	return response

@home.route('/agency/<agency_id>')
def get_agency(agency_id):
	agency = Agency.query.get_or_404(agency_id)
	routes = Route.query.filter(Route.agency_id == agency_id).order_by(Route.route_short_name).all()
	return render_template('home/agency.html', agency=agency, routes=routes)

@home.route('/routes/<route_id>')
def get_route(route_id):
	route = Route.query.get_or_404(route_id)
	trips = Trip.query.filter(Trip.route_id == route_id)\
		.order_by(Trip.card_code, Trip.direction_id, Trip.trip_headsign).all()
	return render_template('home/route.html', route=route, trips=trips)

@home.route('/stops/<stop_id>')
def get_stop(stop_id):
	stop = Stop.query.get_or_404(stop_id)
	routes = db.session.query(Route)\
		.join(Trip, Route.route_id==Trip.route_id)\
		.join(StopSeq, StopSeq.trip_id == Trip.trip_id)\
		.filter(StopSeq.stop_id==stop_id)\
		.order_by(Route.route_short_name)\
		.all()

	return render_template('home/stop.html', stop=stop, routes=routes)

@home.route('/routes/<route_id>/trips/<trip_id>')
def get_trip(route_id, trip_id):
	trip = Trip.query.get_or_404(trip_id)
	route = Route.query.get_or_404(route_id)

	used_services = db.session.query(TripStartTime.service_id)\
		.filter_by(trip_id=trip_id).distinct().subquery()

	services = Calendar.query.\
		filter(Calendar.service_id.in_(used_services)).all()

	stop_seq_query = db.session.query(Stop, StopSeq).\
		join(StopSeq, Stop.stop_id == StopSeq.stop_id).\
		filter(StopSeq.trip_id == trip_id).\
		order_by(StopSeq.stop_sequence).all()

	return render_template('home/trip/index.html', trip=trip, route=route,\
		services=services, sequence=stop_seq_query)

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

		for stop_time in offset_sequence_times(stop_sequence, startTimeRow.start_time):
			times.append(stop_time['arrival_time'])

		trip_times.append(times)


	time_table = zip(stops, *trip_times)

	return render_template('home/trip/services.html', trip=trip, stops=stops,\
		trip_start_times=trip_start_times, time_table=time_table, route=route,\
		service=service)

