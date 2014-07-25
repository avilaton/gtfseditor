#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import codecs

from keyholemarkup import Kml

def readParadas(filename):
	paradas = {}
	with open(filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			paradas[row['stop_id']] = row
	return paradas

def readParadasPorRecorrido(filename):
	with open(filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		trip_ids = [t for t in reader.fieldnames]
		trip_ids.remove('stop_id')
		trip_stops = {f:[] for f in trip_ids}

		for r in reader:
			for trip_id in trip_ids:
				if r[trip_id]:
					trip_stops[trip_id].append(r['stop_id'])

	return trip_stops

if __name__ == '__main__':
	# readers
	paradas = readParadas('ersa/paradas.csv')
	trip_stops = readParadasPorRecorrido('ersa/paradas_por_recorrido.csv')

	kml = Kml('ersa/paradas.kml')
	kml.findPlacemarks()
	rows = []
	for p in kml.placemarks:
		stop_id = codecs.encode(p['name'].title(),'utf8')
		try:
			parada = paradas[stop_id]
		except:
			print(stop_id + " not found")
		stop_esquina = codecs.decode(parada['stop_esquina'], 'utf-8').title()
		print(codecs.encode(stop_esquina,'utf-8'))
		rows.append({
			'stop_id': codecs.encode(p['name'].title(),'utf8'),
			'stop_lat': p['lat'],
			'stop_lon': p['lon'],
			'stop_calle': codecs.encode(p['description'].title(), 'utf8'),
			'stop_esquina': codecs.encode(stop_esquina,'utf-8')
			})

	# writers
	fields = ['stop_id', 'stop_lat', 'stop_lon', 'stop_calle', 'stop_esquina']
	with open('ersa/stops.txt', 'wb') as csvfile:
		writer = csv.DictWriter(csvfile, fields)
		writer.writeheader()
		writer.writerows(rows)

	with open('ersa/stop_times.txt', 'wb') as csvfile:
		writer = csv.DictWriter(csvfile, ['trip_id', 'stop_id', 'stop_sequence'])
		writer.writeheader()
		for trip_id,stops in trip_stops.items():
			for i, stop_id in enumerate(stops):
				writer.writerow({
					'stop_id': stop_id,
					'trip_id': trip_id,
					'stop_sequence': i+1
					})
