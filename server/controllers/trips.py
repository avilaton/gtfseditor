#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request
from server import app
from server.models import Trip
from server.models import Stop
from server.models import StopSeq
from server import geojson

from collections import defaultdict

@app.get('/api/trip/<trip_id>/stops')
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
		f = geojson.feature(id = stop.stop_id,
			coords = [stop.stop_lon, stop.stop_lat], 
			properties = properties)
		features.append(f)
	return geojson.featureCollection(features)

@app.put('/api/trip/<trip_id>/stops')
def saveTripStops(db, trip_id):
	# if 'q' in request.query:
	# 	if request.query['q'] == 'sort':
	# 		result = tb.sortTripStops(trip_id)
	# 	elif request.query['q'] == 'align':
	# 		result = tb.alignTripStops(trip_id)
	# 	else:
	geojsonTrip = request.json
	featureList = geojsonTrip['features']
	print featureList

	# stops = db.query(StopSeq).filter(StopSeq.trip_id == trip_id).delete()

	# create new ids for new stops
	# for i,f in enumerate(featureList):
	# 	p = defaultdict(str)
	# 	for k,v in f['properties'].items():
	# 		p[k] = v

	# 		if 'id' in f:
	# 			stop_id = f['id']
	# 			stop_seq = p['stop_seq']
	# 		else:
	# 			stop_id = self.getNewStopId()
	# 			stop_seq = 1000+i

	# self.db.insert('stop_seq',trip_id=trip_id,stop_id=stop_id,stop_sequence=stop_seq)

	return {'success':True,'trip_id':trip_id}