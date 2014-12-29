#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Trip
from ..models import Stop
from ..models import StopSeq
from ..models import TripStartTime
from . import api
from sqlalchemy import not_
from server.collections.stop_sequence import StopSequence
@api.route('/trips/') 
def get_alltrips():
    trips = Trip.query.all()
    return jsonify({
        'trips': [item.to_json for item in trips]
    }) 

@api.route('/trips/<id>')
def get_trip(id):
    item = Trip.query.get_or_404(id)
    return jsonify(item.to_json)

@api.route('/trips/<id>', methods=['PUT'])
def edit_trip(id):
	data = request.json
	item = Trip.query.get_or_404(data.get('trip_id'))
	item = Trip(**data)
	db.session.merge(item)
	return jsonify(item.to_json)

@api.route('/trips/', methods=['POST']) 
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


@api.route('/trips/<trip_id>/stops.json', methods=['GET'])
def tripStops(trip_id):
	rows = db.session.query(Stop, StopSeq).join(StopSeq, Stop.stop_id == StopSeq.stop_id).filter(StopSeq.trip_id == trip_id).order_by(StopSeq.stop_sequence).all()
	features = []
	for row in rows:
		stop = row.Stop
		stop_seq = row.StopSeq
		features.append({'stop': row.Stop.to_json,'stop_seq': row.StopSeq.to_json}) 
	return {'rows': "features"}

@api.route('/trips/<trip_id>/stops.json', methods=['PUT'])
def tripStopsPut(trip_id):
	data = request.json
	print data
	rows = data['rows'] 
	for row in rows:
		row.pop('speed', None)
		stopSeq = StopSeq(**row)
		db.session.merge(stopSeq)
	return {'success':True,'trip_id':trip_id} 

@api.route('/trips/<trip_id>/stops.geojson', methods=['PUT'])
def saveTripStops(trip_id):
	geojson = request.json
	featureList = geojson['features'] 
	
	stop_ids = set([])
	rows = []
	for item in featureList:
		properties = item["properties"]
		stop_ids.add(str(properties["stop_id"]))
		data = {
			'trip_id': trip_id,
			"stop_sequence": properties["stop_seq"],
			"stop_id": properties["stop_id"]
		}
		rows.append(data)

	removedStops = db.session.query(StopSeq).filter(StopSeq.trip_id == trip_id,not_(StopSeq.stop_id.in_(stop_ids))).all()
	for stopSeq in removedStops:
		db.session.remove(stopSeq)

	for row in rows:
		stopSeq = StopSeq(**row)
		db.session.merge(stopSeq)
	
	return {'success':True,'trip_id':trip_id} 

@api.route('/trips/<trip_id>/actions/sort-stops', methods=['GET', 'OPTIONS'])
def sortTripStops( trip_id):
	stopSequence = StopSequence(trip_id)
	stopSequence.sortStops() 
	return {'success': True} 

@api.route('/trips/<trip_id>/actions/update-dist', methods=['GET'])
def sortTripStopsUpdate(trip_id):
	stopSequence = StopSequence(trip_id)
	stopSequence.updateDistances()
	return {'success': True}

@api.route('/trips/<trip_id>/start-times.json', methods=['GET'])
def tripStopsStartTimes(trip_id):
	rows = db.session.query(TripStartTime).filter(TripStartTime.trip_id == trip_id).\
		order_by(TripStartTime.service_id, TripStartTime.start_time).all()

	features = [row.to_json for row in rows]
	return {'rows': features} 

@api.route('/trips/<trip_id>/start-times.json', methods=['PUT'])
def updateTripStartTimes(trip_id):
	data = request.json
	db.session.query(TripStartTime).filter(TripStartTime.trip_id == trip_id).delete()
	for item in data['rows']:
		tripStartTime = TripStartTime(**item)
		db.session.merge(tripStartTime)
	return {'success': True}

@api.route('/trips/<trip_id>/start-times.csv', methods=['POST'])
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

	return {'success': True} 