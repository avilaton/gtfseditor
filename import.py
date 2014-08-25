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

def importTable(db, Model, filename):
	logger.info("Importing " + Model.__tablename__ + " from : %s", filename)
	with open(filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		keyMap = {field:field for field in reader.fieldnames}
		for row in reader:
			d = {outKey:codecs.decode(row[inKey],'utf8') for inKey, outKey in keyMap.items()}
			model = Model(**d)
			db.merge(model)
	db.commit()

def importStops(db, filename):
	logger.info("Importing stops from : %s", filename)
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
	logger.info("Importing trips from : %s", filename)
	keyMap = {
		'ID-recorrido': 'trip_id', 
		'ida-vuelta': 'direction_id',
		'descripcion': 'trip_headsign',
		'destino': 'trip_short_name'}
	with open(filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			codigo = row['route-trip']
			route_id = codigo[:-3]
			if route_id.isdigit():
				route_id = route_id.zfill(3)
			d = {outKey:codecs.decode(row[inKey],'utf8') for inKey, outKey in keyMap.items()}
			d['route_id'] = route_id
			trip = Trip(**d)
			trip.shape_id = trip.trip_id
			db.merge(trip)
	db.commit()

def importRoutes(db, filename):
	logger.info("Importing routes from : %s", filename)
	with open(filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			codigo = row['route-trip']
			route_id = codigo[:-3]
			if route_id.isdigit():
				route_id = route_id.zfill(3)
			d = {}
			d['route_id'] = route_id
			# d['route_short_name'] = codecs.decode(row['descripcion'],'utf8')
			d['route_short_name'] = route_id
			d['route_type'] = 'Bus'
			d['route_desc'] = codecs.decode(row['descripcion'],'utf8')
			route = Route(**d)

			db.merge(route)
	db.commit()

def importShapes(db, filename):
	logger.info("Importing shapes from : %s", filename)
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
	logger.info("Importing stop_times from : %s", filename)
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

if __name__ == '__main__':
	Session = sessionmaker(bind=engine)
	db = scoped_session(Session)
	FOLDER = 'incoming/mza/'

	importTable(db, Agency, FOLDER + 'agency.csv')
	importTable(db, FeedInfo, FOLDER + 'feed_info.csv')
	importTable(db, Calendar, FOLDER + 'calendar.csv')
	importTable(db, CalendarDate, FOLDER + 'calendar_dates.csv')
	
	importStops(db, FOLDER + 'stops.csv')
	importTrips(db, FOLDER + 'routes-trips-clean.csv')
	importRoutes(db, FOLDER + 'routes-trips-clean.csv')
	importShapes(db, FOLDER + 'shapes-raw.csv')
	importStopTimes(db, FOLDER + 'stop_times.csv')

	importTable(db, TripStartTime, FOLDER + 'trips_start_times.csv')

	# please run manage.py to generate shape-pt-sequence
	# and stop_sequence
