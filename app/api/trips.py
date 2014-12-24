#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Trip
from . import api


@api.route('/trips/') #LISTO
def get_alltrips():
    trips = Trip.query.all()
    return jsonify({
        'trips': [item.to_json for item in trips]
    }) 

@api.route('/trips/<id>') #LISTO
def get_trip(id):
    item = Trip.query.get_or_404(id)
    return jsonify(item.to_json)

@api.route('/trips/<id>', methods=['PUT'])#LISTO
def edit_trip(id):
	data = request.json
	item = Trip.query.get_or_404(data.get('trip_id'))
	item = Trip(**data)
	db.session.merge(item)
	return jsonify(item.to_json)

@api.route('/trips/', methods=['POST']) #LISTO
def add_trip():
	data = request.json
	trip = Trip(**data)
	db.session.add(trip)
	db.session.commit()
	print "###", trip.route_id
	return jsonify(trip.to_json), 201,{'Location': url_for('api.get_trip', id=trip.route_id, _external=True)}

@api.route('/trips/<id>', methods=['DELETE'])
def deleteTrip(id):		
	trip = Trip.query.filter_by(trip_id = id).one()
	db.session.delete(trip)
	db.session.commit()
	return jsonify({'status': 'success'}), 200