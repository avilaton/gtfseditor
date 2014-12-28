#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import csv

from bottle import request
from bottle import abort
from server import app
from server.models import Trip
from server.models import Stop
from server.models import StopSeq
from server.models import TripStartTime
from server.collections.stop_sequence import StopSequence
from server import geojson

from collections import defaultdict
from sqlalchemy import not_

@app.route('/api/trips/<trip_id>', method=['PUT', 'OPTIONS'])
def updateTrip(db, trip_id):
	data = request.json
	trip = Trip(**data)
	db.merge(trip)
	return trip.as_dict #LISTO

@app.route('/api/trips', method=['POST', 'OPTIONS'])
def createTrip(db):
	data = request.json
	trip = Trip(**data)
	db.add(trip)
	return trip.as_dict #LISTO

@app.route('/api/trips/<trip_id>', method=['DELETE', 'OPTIONS'])
def deleteTrip(db, trip_id):
	route = db.query(Trip).filter(Trip.trip_id == trip_id).one()
	db.delete(route)
	return {'success': True} #LISTO

@app.route('/api/trips/<trip_id>/stops.geojson', method=['GET', 'OPTIONS'])
def tripStops(db, trip_id):
	rows = db.query(Stop, StopSeq).join(StopSeq, Stop.stop_id == StopSeq.stop_id)\
		.filter(StopSeq.trip_id == trip_id)\
		.order_by(StopSeq.stop_sequence).all()

	features = []
	for row in rows:
		stop = row.Stop
		stop_seq = row.StopSeq
		properties = stop.as_dict
		properties.update({'stop_seq': stop_seq.stop_sequence})
		properties.update({'stop_time': stop_seq.stop_time})
		properties.update({'shape_dist_traveled': stop_seq.shape_dist_traveled})
		f = geojson.feature(id = stop.stop_id,
			coords = [stop.stop_lon, stop.stop_lat], 
			properties = properties)
		features.append(f)
	return geojson.featureCollection(features)

@app.route('/api/trips/<trip_id>/stops.json', method=['GET', 'OPTIONS'])
def tripStops(db, trip_id):
	rows = db.query(Stop, StopSeq).join(StopSeq, Stop.stop_id == StopSeq.stop_id)\
		.filter(StopSeq.trip_id == trip_id).order_by(StopSeq.stop_sequence).all()

	features = []
	for row in rows:
		stop = row.Stop
		stop_seq = row.StopSeq
		features.append({
			'stop': row.Stop.as_dict,
			'stop_seq': row.StopSeq.as_dict
			})
	return {'rows': features} #no se como importar en flask el as_dict

@app.route('/api/trips/<trip_id>/stops.json', method=['PUT'])
def tripStops(db, trip_id):
	data = request.json
	rows = data['rows'] #No se que parametro es rows, no se como probar con el REST Console
	for row in rows:
		row.pop('speed', None)
		stopSeq = StopSeq(**row)
		db.merge(stopSeq)
	
	return {'success':True,'trip_id':trip_id} # LISTO pero sin testear, 

@app.route('/api/trips/<trip_id>/stops.geojson', method=['PUT', 'OPTIONS'])
def saveTripStops(db, trip_id):
	geojson = request.json
	featureList = geojson['features'] #No se que parametro es features, no se como probar con el REST Console
	
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

	removedStops = db.query(StopSeq).filter(StopSeq.trip_id == trip_id, 
		not_(StopSeq.stop_id.in_(stop_ids))).all()
	for stopSeq in removedStops:
		db.remove(stopSeq)

	for row in rows:
		stopSeq = StopSeq(**row)
		db.merge(stopSeq)
	
	return {'success':True,'trip_id':trip_id} #LISTO pero sin testear

@app.route('/api/trips/<trip_id>/actions/sort-stops', method=['GET', 'OPTIONS'])
def sortTripStops(db, trip_id):
	stopSequence = StopSequence(trip_id)
	stopSequence.sortStops()
	return {'success': True} #Listo pero con errores

@app.route('/api/trips/<trip_id>/actions/update-dist', method=['GET', 'OPTIONS'])
def sortTripStops(db, trip_id):
	stopSequence = StopSequence(trip_id)
	stopSequence.updateDistances()
	return {'success': True} #Listo pero con errores

@app.route('/api/trips/<trip_id>/start-times.json', method=['GET', 'OPTIONS'])
def tripStops(db, trip_id):
	rows = db.query(TripStartTime).filter(TripStartTime.trip_id == trip_id).\
		order_by(TripStartTime.service_id, TripStartTime.start_time).all()

	features = [row.as_dict for row in rows]
	return {'rows': features} #Listo pero falta as_dict

@app.route('/api/trips/<trip_id>/start-times.json', method=['PUT', 'OPTIONS'])
def updateTripStartTimes(db, trip_id):
	data = request.json
	db.query(TripStartTime).filter(TripStartTime.trip_id == trip_id).delete()
	for item in data['rows']:
		tripStartTime = TripStartTime(**item)
		db.merge(tripStartTime)
	return {'success': True}

@app.route('/api/trips/<trip_id>/start-times.csv', method=['POST'])
def uploadTripStartTimes(db, trip_id):
	fileUpload = request.files.get('upload')
	filename = fileUpload.filename

	reader = csv.DictReader(fileUpload.file)
	if len(reader.fieldnames) is not 2 or 'start_time' not in reader.fieldnames or\
		'service_id' not in reader.fieldnames:
		abort(400)

	db.query(TripStartTime).filter(TripStartTime.trip_id == trip_id).delete()

	if db.query(Trip).filter(Trip.trip_id == trip_id).count():
		for row in reader:
			row['trip_id'] = trip_id
			startTime = TripStartTime(trip_id = trip_id,
				start_time = row['start_time'],
				service_id = row['service_id'])
			db.merge(startTime)
	else:
		abort(404, 'trip not found')

	return {'success': True}
