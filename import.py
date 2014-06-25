#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   import.py
#	   
#	   Copyright 2012 Gaston Avila <avila.gas@gmail.com>
#	   
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 2 of the License, or
#	   (at your option) any later version.
#	   
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#	   
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import csv
import codecs

from server import engine
from server.models import *
from sqlalchemy.orm import sessionmaker, scoped_session

def importStops(db, filename):
	keyMap = {
		'stop_id': 'stop_id', 
		'stop_lat': 'stop_lat',
		'stop_lon': 'stop_lon',
		'entre': 'stop_entre', 
		'calle': 'stop_calle', 
		'numero': 'stop_numero', 
		'stop_name': 'stop_name'
		}
	with open(filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			d = {outKey:codecs.decode(row[inKey],'utf8') for inKey, outKey in keyMap.items()}
			d.update({
				'stop_lat': float(row['stop_lat']),
				'stop_lon': float(row['stop_lon'])
				})
			stop = Stop(**d)
			db.merge(stop)
	db.commit()

def importTrips(db, filename):
	keyMap = {
		'trip_id': 'trip_id', 
		'route_id': 'route_id',
		# 'route_name': 'route_name',
		'direction_id': 'direction_id',
		# 'active': 'active',
		# 'codigo': 'codigo',
		'trip_headsign': 'trip_headsign',
		'trip_short_name': 'trip_short_name'}
	with open(filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			d = {outKey:codecs.decode(row[inKey],'utf8') for inKey, outKey in keyMap.items()}
			trip = Trip(**d)
			trip.shape_id = trip.trip_id
			db.merge(trip)
	db.commit()

def importRoutes(db, filename):
	keyMap = {
		'route_id': 'route_id',
		'route_name': 'route_short_name',
		'active': 'active'
		}
	with open(filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			d = {outKey:codecs.decode(row[inKey],'utf8') for inKey, outKey in keyMap.items()}
			route = Route(**d)
			db.merge(route)
	db.commit()

def importShapes(db, filename):
	# errorsFile = open('errors.log', 'w')
	# errorsLog = csv.DictWriter(errorsFile)
	# errorsLog.write
	keyMap = {
		"shape_id": "shape_id",
		"shape_pt_lat": "shape_pt_lat",
		"shape_pt_lon": "shape_pt_lon",
		# "direction": "direction",
		"time": "shape_pt_time",
		}
	rows = []
	engine.execute(Shape.__table__.delete())
	ins = Shape.__table__.insert()
	with open(filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for i, row in enumerate(reader):
			d = {outKey:row[inKey] for inKey, outKey in keyMap.items()}
			lat, lon = d['shape_pt_lat'], d['shape_pt_lon']
			try:
				lat, lon = float(lat), float(lon)
			except Exception, e:
				logger.info("droped point", d)
				continue
			try:
				assert lat > -180
				assert lat < 180
				assert lon < 90
				assert lon > -90
			except Exception, e:
				logger.info("invalid coords")
				logger.info(d)
				continue
			d.update({'shape_pt_lat': lat, 'shape_pt_lon': lon, 
				'shape_pt_sequence': i + 300000})
			rows.append(d)

	engine.execute(ins, rows)
	logger.info("done importing shapes")

def importStopTimes(db, filename):
	keyMap = {
		"stop_id": "stop_id",
		"trip_id": "trip_id",
		"time": "stop_time"
		}
	rows = []
	engine.execute(StopSeq.__table__.delete())
	ins = StopSeq.__table__.insert()
	with open(filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for i, row in enumerate(reader):
			d = {outKey:row[inKey] for inKey, outKey in keyMap.items()}
			d.update({'stop_sequence': i + 100000})
			rows.append(d)

	engine.execute(ins, rows)
	logger.info("done importing stop times")

def generateShapePtSequence(db):
	ins = Shape.__table__.insert()
	for shape in db.query(Shape.shape_id).distinct():
		
		logger.info("generate sequence for shape_id: %s", shape.shape_id)

		shapeQuery = db.query(Shape).filter_by(shape_id = shape.shape_id)
		shape_pts = shapeQuery.order_by(Shape.shape_pt_time)

		pts = []
		for i, pt in enumerate(shape_pts):
			pt.shape_pt_sequence = i
			pts.append(pt.as_dict)
			db.delete(pt)
		# db.commit()
		db.execute(ins, pts)

	db.commit()

def generateStopSeq(db):
	logger.info("Generating Stop Sequences")

	import time
	t0 = time.time()

	ins = StopSeq.__table__.insert()
	for trip in db.query(StopSeq.trip_id).distinct():
		
		logger.info("generate sequence for trip_id: %s", trip.trip_id)

		query = db.query(StopSeq).filter_by(trip_id = trip.trip_id)
		trip_pts = query.order_by(StopSeq.stop_time)

		pts = []
		for i, pt in enumerate(trip_pts):
			pt.stop_sequence = i
			pts.append(pt.as_dict)
			db.delete(pt)
		db.execute(ins, pts)

	db.commit()
	logger.info("Time elapsed %s",time.time()-t0)

if __name__ == '__main__':
	Session = sessionmaker(bind=engine)
	db = scoped_session(Session)
	importStops(db, 'incoming/mza/stops.csv')
	importTrips(db, 'incoming/mza/trips.csv')
	importRoutes(db, 'incoming/mza/trips.csv')
	importShapes(db, 'incoming/mza/shapes-raw.csv')
	importStopTimes(db, 'incoming/mza/stop_times.csv')
	generateShapePtSequence(db)
	generateStopSeq(db)
