#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from flask import jsonify, request, g, abort, url_for
from flask import Response
from flask import json
from .. import db
from ..models import Trip
from ..models import Stop
from ..models import StopSeq
from ..models import TripStartTime
from . import api
from sqlalchemy import not_
from app.services.sequence import StopSequence
from .decorators import admin_required


@api.route('/trips/')
def get_alltrips():
    trips = Trip.query.all()
    return Response(json.dumps([i.to_json for i in trips]),
        mimetype='application/json')


@api.route('/trips/<id>')
def get_trip(id):
    item = Trip.query.get_or_404(id)
    return jsonify(item.to_json)


@api.route('/trips/<id>', methods=['PUT'])
@admin_required
def edit_trip(id):
	data = request.json
	item = Trip.query.get_or_404(data.get('trip_id'))
	item = Trip(**data)
	db.session.merge(item)
	db.session.commit()
	return jsonify(item.to_json)


@api.route('/trips/', methods=['POST']) 
@admin_required
def add_trip():
	data = request.json
	trip = Trip(**data)
	db.session.add(trip)
	db.session.commit()
	return jsonify(trip.to_json), 201, {'Location': url_for('api.get_trip',
		id=trip.trip_id, _external=True)}


@api.route('/trips/<id>', methods=['DELETE'])
@admin_required
def deleteTrip(id):
	trip = Trip.query.filter_by(trip_id = id).one()
	db.session.delete(trip)
	db.session.commit()
	return jsonify({'status': 'success'}), 200


@api.route('/trips/<trip_id>/stops.json', methods=['GET'])
def tripStops(trip_id):
	rows = db.session.query(Stop, StopSeq).join(StopSeq, Stop.stop_id == StopSeq.stop_id).filter(StopSeq.trip_id == trip_id).order_by(StopSeq.stop_sequence).all()
	features = []
	for row in rows:
		stop = row.Stop
		stop_seq = row.StopSeq
		features.append({'stop': row.Stop.to_json,'stop_seq': row.StopSeq.to_json}) 
	return jsonify({'rows': features})


@api.route('/trips/<trip_id>/stops.json', methods=['PUT'])
@admin_required
def tripStopsPut(trip_id):
	data = request.json
	items = data['rows']

	stop_ids = set([])
	rows = []
	for item in items:
		stop_ids.add(str(item["stop_id"]))
		rows.append(item)

	removedStops = db.session.query(StopSeq).filter(StopSeq.trip_id == trip_id, \
		not_(StopSeq.stop_id.in_(stop_ids))).all()

	for stopSeq in removedStops:
		print stopSeq
		db.session.delete(stopSeq)

	for row in rows:
		stopSeq = StopSeq(**row)
		db.session.merge(stopSeq)

	db.session.commit()

	return jsonify({'success':True,'trip_id':trip_id})


@api.route('/trips/<trip_id>/actions/sort-stops', methods=['GET'])
@admin_required
def sortTripStops( trip_id):
	stopSequence = StopSequence(trip_id)
	stopSequence.sortStops() 
	return jsonify({'success': True})


@api.route('/trips/<trip_id>/actions/update-dist', methods=['GET'])
@admin_required
def sortTripStopsUpdate(trip_id):
	stopSequence = StopSequence(trip_id)
	stopSequence.updateDistances()
	return jsonify({'success': True})


@api.route('/trips/<trip_id>/actions/interpolate-times', methods=['GET'])
@admin_required
def interpolateTimes(trip_id):
	stopSequence = StopSequence(trip_id)
	stopSequence.interpolateTimes()
	return jsonify({'success': True})


@api.route('/trips/<trip_id>/start-times.json', methods=['GET'])
def tripStopsStartTimes(trip_id):
	rows = db.session.query(TripStartTime).filter(TripStartTime.trip_id == trip_id).\
		order_by(TripStartTime.service_id, TripStartTime.start_time).all()

	features = [row.to_json for row in rows]
	return jsonify({'rows': features})


@api.route('/trips/<trip_id>/calendars/<service_id>/start-times.json', methods=['GET'])
def tripServiceTimes(trip_id, service_id):
	rows = db.session.query(TripStartTime).\
		filter_by(trip_id=trip_id, service_id=service_id).\
		order_by(TripStartTime.start_time).all()

	return Response(json.dumps([row.to_json for row in rows]),  mimetype='application/json')


@api.route('/trips/<trip_id>/calendars/<service_id>/start-times.json', methods=['PUT'])
def updateTripStartTimes(trip_id, service_id):
	data = request.json
	db.session.query(TripStartTime).filter_by(trip_id=trip_id, service_id=service_id).delete()
	for item in data:
		tripStartTime = TripStartTime(**item)
		db.session.merge(tripStartTime)
	db.session.commit()
	return jsonify({'success': True})


@api.route('/trips/<trip_id>/start-times.csv', methods=['POST'])
@admin_required
def uploadTripStartTimes(db, trip_id):
	fileUpload = request.files.get('upload')
	filename = fileUpload.filename

	reader = csv.DictReader(fileUpload.file)
	if len(reader.fieldnames) is not 2 or 'start_time' not in reader.fieldnames or\
		'service_id' not in reader.fieldnames:
		abort(400)

	db.session.query(TripStartTime).filter(TripStartTime.trip_id == trip_id).delete()

	if db.session.query(Trip).filter(Trip.trip_id == trip_id).count():
		for row in reader:
			row['trip_id'] = trip_id
			startTime = TripStartTime(trip_id = trip_id,
				start_time = row['start_time'],
				service_id = row['service_id'])
			db.session.merge(startTime)
	else:
		abort(404, 'trip not found')

	return jsonify({'success': True})
