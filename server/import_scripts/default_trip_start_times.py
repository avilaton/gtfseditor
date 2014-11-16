#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from datetime import date, datetime, time, timedelta

def main():
	rows = []

	initTime = datetime.combine(date.today(), time(6, 0))
	finalTime = datetime.combine(date.today(), time(23, 0))

	curTime = initTime
	i = 0
	while curTime < finalTime:
		curTime = initTime + timedelta(minutes=30)*i
		model = {
			'start_time': curTime.strftime('%H:%M:%S'),
			'trip_id': 'default',
			'service_id': 'default'
			}
		rows.append(model)
		i += 1
	with open('trips_start_times.csv', 'w') as out:
		writer = csv.DictWriter(out, fieldnames=['start_time', 'trip_id', 'service_id'])
		writer.writeheader()
		writer.writerows(rows)

if __name__ == '__main__':
	main()