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
from gtfstools import utils

class Coniferal(object):
	"""docstring for Coniferal"""
	def __init__(self, db):
		self.db = db
		
	def importStops(self):
		changed = []
		self.db.query("SELECT * FROM paradasConiferal")
		newStops = self.db.cursor.fetchall()
		for newStop in newStops:
			stop_id = newStop['stop_id']
			# if newStop['stop_id'] != "C0004":
			# 	continue
			self.db.query("SELECT * FROM stops WHERE stop_id='{stop_id}'".format(stop_id=stop_id))
			oldStop = self.db.cursor.fetchall()[0]
			p1 = {'lat': newStop['stop_lat'], 'lon': newStop['stop_lon']}
			p2 = {'lat': oldStop['stop_lat'], 'lon': oldStop['stop_lon']}
			distance = utils.haversineDict(p1,p2)
			changed.append({
				'stop_id': stop_id,
				'distance': distance
				})
			if distance > 5:
				print("analysing stop: " + newStop['stop_id'])
				print distance
				print oldStop['stop_calle'] == newStop['stop_calle']
		newlist = sorted(changed, key=lambda k: k['distance']) 
		return newlist

	def importTripStops(self):
		self.db.query("SELECT * FROM paradasConiferal")
		trips = {}
		for r in self.db.cursor.fetchall():
			stop_id = str(r['stop_id'])
			r = r['lineas'].strip().split('-')
			r = filter(lambda x: x, map(unicode.strip, r))
			r = map(str.lower, map(str, r))
			r = map(lambda x: x.replace(' ', '.'),r)
			for trip_id in r:
				if trip_id not in trips:
					trips.update({trip_id: [stop_id]})
				else:
					trips[trip_id].append(stop_id)
		for trip_id in trips:
			print trip_id, trips[trip_id]

if __name__ == '__main__':
	db = o.dbInterface('../database/cba-1.0.0.sqlite')


	coniferal = Coniferal(db)

	# changed = coniferal.importStops()
	# print changed
	coniferal.importTripStops()

	db.close()