#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import redirect,g, abort, url_for, current_app,render_template
from .. import db, admin
from ..models import Agency
from ..models import Route
from ..models import Trip
from . import home

@home.route('/')
def index():
	agencies = Agency.query.all()
	routes = Route.query.order_by(Route.route_id).all()
	return render_template('home/index.html', agencies=agencies, routes=routes)

@home.route('/agency/<agency_id>')
def get_agency(agency_id):
	agencies = Agency.query.all()
	return render_template('home/index.html', agencies=agencies)

@home.route('/routes/<route_id>')
def get_route(route_id):
	route = Route.query.get_or_404(route_id)
	trips = Trip.query.filter(Trip.route_id == route_id)\
        .order_by(Trip.trip_headsign).all()
	return render_template('home/route.html', route=route, trips=trips)
