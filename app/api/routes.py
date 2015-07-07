#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app
from flask import json
from flask import Response
from .. import db
from ..models import Route
from ..models import Trip
from . import api
from .decorators import admin_required


@api.route('/routes/')
def get_routes():
    routes = Route.query.order_by(Route.route_short_name).all()
    return Response(
        json.dumps([item.to_json for item in routes]),
        mimetype='application/json')


@api.route('/routes/<id>')
def get_route(id):
    item = Route.query.get_or_404(id)
    return jsonify(item.to_json)


@api.route('/routes/', methods=['POST'])
@admin_required
def add_route():
    item = Route(**request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json), 201, \
        {'Location': url_for('api.get_route', id=item.route_id, _external=True)}

@api.route('/routes/<id>', methods=['PUT'])
@admin_required
def edit_route(id):
    data = request.json
    item = Route.query.get_or_404(data.get('route_id'))
    item = Route(**data)
    db.session.merge(item)
    db.session.commit()
    return jsonify(item.to_json)


@api.route('/routes/<id>', methods=['DELETE'])
@admin_required
def delete_route(id):
    route = Route.query.filter_by(route_id = id).one()
    db.session.delete(route)
    db.session.commit()
    return jsonify({'status': 'success'}), 200


@api.route('/route/<route_id>/trips')
def get_route_trips(route_id):
    trips = Trip.query.filter(Trip.route_id == route_id)\
        .order_by(Trip.card_code, Trip.direction_id, Trip.trip_headsign).all()
    return Response(
        json.dumps([i.to_json for i in trips]),
        mimetype='application/json')