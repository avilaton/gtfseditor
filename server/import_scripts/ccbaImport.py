#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import codecs

from keyholemarkup import Kml

def getStopsFromKml():	
	kml = Kml('ccba/paradas.kml')
	kml.findPlacemarks()
	stops = {}
	for p in kml.placemarks:
		stop_id = p['name'][1:]
		if stop_id not in stops:
			stops[stop_id] = p
		else:
			print("already exists")
			print stops[stop_id]
			print p

	print len(kml.placemarks)
	print("Total unique stops in kml: "+ str(len(stops.items())))
	return stops

def matchTableToKml():
	stopsKml = getStopsFromKml()

	uniqueInCsv = {}
	coordsNotFound = []
	coordsFound = []
	with open('ccba/stops_table.csv', 'r') as csvfile:
		stopsCsv = csv.DictReader(csvfile)
		fieldnames = stopsCsv.fieldnames

		for stop in stopsCsv:
			stop_id = stop['stop_id']
			uniqueInCsv[stop_id] = stop

	for stop_id, stop in uniqueInCsv.items():
		if stop_id in stopsKml:
			coordinates = stopsKml[stop_id]
			stop['stop_lat'] = coordinates['lat']
			stop['stop_lon'] = coordinates['lon']
			coordsFound.append(stop)
		else:
			#print("not found")
			coordsNotFound.append(stop)

	print("Total not found coordinates: "+ str(coordsNotFound))
	print(coordsNotFound)

	with open('ccba/stops_not_found.csv', 'wb') as csvfile:
		stopsCsv = csv.DictWriter(csvfile, fieldnames)
		stopsCsv.writeheader()
		for stop in coordsNotFound:
			stopsCsv.writerow(stop)

	fieldnames.append('stop_lat')
	fieldnames.append('stop_lon')
	with open('ccba/stops.csv', 'wb') as csvfile:
		stopsCsv = csv.DictWriter(csvfile, fieldnames)
		stopsCsv.writeheader()
		for stop in coordsFound:
			stopsCsv.writerow(stop)

def buildSequenceNumbers():
	rows = []
	with open('ccba/trip_stops.csv', 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		fieldnames = reader.fieldnames
		i = 1
		prev = None
		for r in reader:
			rows.append(r)
			if prev:
				if prev['trip_id'] == r['trip_id']:
					i += 1
				else:
					i = 1
			r['stop_sequence'] = i
			prev = r

	with open('ccba/stop_times.csv', 'wb') as csvfile:
		fieldnames.append('stop_sequence')
		writer = csv.DictWriter(csvfile, fieldnames)
		writer.writeheader()
		writer.writerows(rows)


if __name__ == '__main__':
	matchTableToKml()
	buildSequenceNumbers()