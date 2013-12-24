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

import ormgeneric as o


def importRoutes(db):
	db.query("""SELECT DISTINCT route_id FROM trips""")
	routesList = [r['route_id'] for r in db.cursor.fetchall()]
	for route_id in routesList:
		trips = db.select('trips', route_id=route_id)
		print(route_id, trips[0]['route_name'])
		db.insert('routes',route_id=route_id, route_short_name=trips[0]['route_name'], agency_id='secretaria')

def generateSeq(db):
	db.query("""SELECT DISTINCT shape_id FROM shapes_raw""")
	shapes = [r['shape_id'] for r in db.cursor.fetchall()]
	for shape_id in shapes:
		print(shape_id)
		db.query("""SELECT * FROM shapes_raw 
			WHERE shape_id={shape_id} 
			ORDER BY time""".format(shape_id=shape_id))
		shape_pts = [dict(r) for r in db.cursor.fetchall()]
		for i, pt in enumerate(shape_pts):
			print(pt)
			db.insert('shapes',
				shape_id=shape_id,
				shape_pt_lon = pt['shape_pt_lon'],
				shape_pt_lat = pt['shape_pt_lat'],
				shape_pt_sequence=i)

def generateStopSeq(db):
	import time
	t0 = time.time()
	db.query("""SELECT DISTINCT trip_id FROM stop_seq""")
	trips = [r['trip_id'] for r in db.cursor.fetchall()]
	print("first query", time.time()-t0)

	t1 = time.time()
	for trip_id in trips:

		db.query("""SELECT * FROM stop_seq 
			WHERE trip_id={trip_id} 
			ORDER BY time""".format(trip_id=trip_id))
		trip_stops = [dict(r) for r in db.cursor.fetchall()]

		for i, pt in enumerate(trip_stops):
			db.query("""UPDATE stop_seq SET stop_sequence={stop_sequence} 
				WHERE trip_id="{trip_id}"
				AND stop_id="{stop_id}";""".format(
					trip_id=trip_id,
					stop_id=pt['stop_id'], 
					stop_sequence=i))
		print("elapsed for: \t" + trip_id +'\t '+ str(time.time()-t1))
		t1 = time.time()

def generateServices(db):
	salidas = [r for r in db.select('salidas', trip_id="1640")]
	print(salidas)
	# UPDATE routes SET active=1 WHERE route_id IN
	# 	(SELECT route_id FROM trips 
	# 	   WHERE trip_id in (select distinct trip_id from salidas)
	# 	)
	pass

if __name__ == '__main__':
	db = o.dbInterface('database/dbRecorridos.sqlite')
	# importRoutes(db)
	# generateSeq(db)
	# generateStopSeq(db)
	generateServices(db)

	db.close()