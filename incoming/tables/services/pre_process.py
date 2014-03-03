#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

def readFrec(filename, service_id, franjas):
	frequencies = []
	with open('frecuencias.csv') as csvFranjas:
		reader = csv.DictReader(csvFranjas)
		for row in reader:
			route_id = row['route_id']
			# print("adding route:" + route_id)
			for franja in franjas:
				st = franja['start_time']
				et = franja['end_time']
				freq = row[franja['modo']]
				if freq:
					headway_secs = int(freq)*60
					print route_id, st, et, headway_secs
					frequencies.append({
						'route_id': route_id, 
						'start_time': st, 
						'end_time': et, 
						'headway_secs': headway_secs,
						'service_id': service_id
						})
	return frequencies

def main():
	franjas = []
	with open('franjas.csv') as csvFrec:
		reader = csv.DictReader(csvFrec)
		for row in reader:
			franjas.append(row)

	frequencies = []
	frequencies.extend(readFrec('frecuencias.csv', 'H', franjas))
	frequencies.extend(readFrec('frecuencias.csv', 'S', franjas))
	frequencies.extend(readFrec('frecuencias.csv', 'D', franjas))

	with open('services.csv', 'wb') as output:
		writer = csv.DictWriter(output, fieldnames=frequencies[0].keys())
		writer.writeheader()
		writer.writerows(frequencies)
	


if __name__ == '__main__':
	main()