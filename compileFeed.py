#!/usr/bin/python
# -*- coding: utf-8 -*-

import transitfeed
import datetime

import ormgeneric.ormgeneric as o


FEED_START_DATE = '20130401'
FEED_END_DATE = '20131231'

def addAgencies(db,schedule,debug=False):
	tz = 'America/Argentina/Cordoba'
	agencyTamse = schedule.AddAgency('Tamse','http://www.tam-se.com.ar',tz,agency_id='tamse')
	agencyConiferal = schedule.AddAgency('Coniferal','http://www.coniferal.com.ar',tz,agency_id='coniferal')
	agencyCcba = schedule.AddAgency(u"Ciudad de Córdoba",'http://www.ccbasacif.com.ar',tz,agency_id='ccba')
	schedule.SetDefaultAgency(agencyTamse)

def addServicePeriods(db,schedule,debug=False):
	#service_period = schedule.GetDefaultServicePeriod()
	
	# Lunes a viernes
	service_H = transitfeed.ServicePeriod()
	service_H.SetServiceId('H')
	service_H.SetWeekdayService(True)
	service_H.SetStartDate(FEED_START_DATE)
	service_H.SetEndDate(FEED_END_DATE)
	schedule.AddServicePeriodObject(service_H)

	# Sabados
	service_S = transitfeed.ServicePeriod()
	service_S.SetServiceId('S')
	service_S.SetDayOfWeekHasService(5)
	service_S.SetStartDate(FEED_START_DATE)
	service_S.SetEndDate(FEED_END_DATE)
	schedule.AddServicePeriodObject(service_S)

	# Domingos y Feriados
	service_D = transitfeed.ServicePeriod()
	service_D.SetServiceId('D')
	service_D.SetDayOfWeekHasService(6)
	service_D.SetStartDate(FEED_START_DATE)
	service_D.SetEndDate(FEED_END_DATE)
	schedule.AddServicePeriodObject(service_D)

def addCalendarDates(db, schedule, debug=False):
	service_H = schedule.GetServicePeriod('H')
	service_S = schedule.GetServicePeriod('S')
	service_D = schedule.GetServicePeriod('D')

	feriados = ['20130101','20130131','20130211','20130212','20130220',
		'20130324','20130329','20130401','20130402','20130501','20130525',
		'20130620','20130621','20130709','20131208','20131225']
	for feriado in feriados:
		wd = datetime.datetime.strptime(feriado,'%Y%m%d').weekday()
		if wd in [0,1,2,3,4]:
			#print feriado,'día habil'
			service_D.SetDateHasService(feriado)
			service_H.SetDateHasService(feriado, has_service=False)
		elif wd == 5:
			#print feriado,'sabado'
			service_D.SetDateHasService(feriado)
			service_S.SetDateHasService(feriado, has_service=False)
		elif wd == 6:
			#print feriado,'domingo'
			service_D.SetDateHasService(feriado)

def addStops(db,schedule,debug=False):
	# q = """SELECT DISTINCT stop_id FROM stop_seq 
	# 	WHERE trip_id="{0}" OR trip_id="{1}" """.format('C0.ida','C0.vuelta')
	if debug:
		q = """SELECT * FROM stops WHERE stop_id IN 
			(SELECT DISTINCT stop_id FROM stop_seq 
				WHERE trip_id='C0.ida')"""
	else:
		q = """SELECT * FROM stops WHERE stop_id IN 
			(SELECT DISTINCT stop_id FROM stop_seq)"""
	
	db.query(q)
	# for s in db.select('stops'):
	for s in db.cursor.fetchall():
		stop = db.select('stops',stop_id=s['stop_id'])[0]
		lat = stop['stop_lat']
		lng = stop['stop_lon']
		if stop['stop_calle']:
			name = stop['stop_calle'] + str(stop['stop_numero'])
		else:
			name = stop['stop_id']
		stop_id = stop['stop_id']
		stop = schedule.AddStop(lat=float(lat),lng=float(lng),name=name,stop_id=stop_id)
		stop.stop_code = stop['stop_id']

def addShapes(db,schedule,debug=False):
	db.query("""SELECT DISTINCT shape_id FROM shapes""")
	for shape in db.cursor.fetchall():
		shape_id = shape['shape_id']
		db.query("""SELECT * FROM shapes WHERE shape_id="{0}" ORDER BY shape_pt_sequence""".format(shape_id))
		l = {'shape_pt_lat':0,'shape_pt_lon':0}
		shapeObject = transitfeed.Shape(shape_id=shape_id)
		for pt in db.cursor.fetchall():
			shapeObject.AddPoint(lat=pt['shape_pt_lat'],lon=pt['shape_pt_lon'])
		schedule.AddShapeObject(shapeObject)

def addRoutes(db,schedule,debug=False):
	for route in db.select('routes'):
		route_id = route['route_id']
		if route_id not in ['C0'] and debug:
			continue
		r = schedule.AddRoute(short_name=route_id, 
			long_name='', 
			route_id=route_id,
			route_type='Bus')

		r.agency_id = route['agency_id']
		#r.route_color = route['route_color']
		#r.route_text_color = route['route_text_color']

def addTrips(db,schedule,debug=False):
	# get servicePeriods
	services = []
	for s in schedule.GetServicePeriodList():
		services.append(s.service_id)
	print 'Service Periods IDs: \n', services

	for r in schedule.GetRouteList():
		route_id = r['route_id']
		for t in db.select('trips', route_id=route_id):
			if t['trip_id'] != 'C0.ida' and debug:
				continue
			for s in services:
				trip_id = t['trip_id'] + '.' + s
				trip = r.AddTrip(trip_id = trip_id,headsign=t['trip_headsign'])
				trip.service_id = s
				print trip
				trip.shape_id = t['trip_id']
				if 'ida' in trip_id:
					trip.direction_id = 0
				elif 'vuelta' in trip_id:
					trip.direction_id = 1

def addStopTimes(db,schedule,debug=False):
	"""Adding Stop Times"""
	for trip in schedule.GetTripList():
		trip_id = trip['trip_id'][:-2]
		# print trip_id
		db.select('timepoints')
		q = """SELECT * FROM stop_seq 
			WHERE trip_id="{0}" 
			ORDER BY stop_sequence""".format(trip_id)
		db.query(q)
		trip_stops = db.cursor.fetchall()
		l = len(trip_stops)

		trip_id = trip_id.replace('V0.','V0H.')
		trip_id = trip_id.replace('N3.Almacenero.','N3.')
		trip_id = trip_id.replace('N3.Warcalde.','N3.')

		db.query("""SELECT key,value FROM timepoints 
			WHERE trip_id='{trip_id}' ORDER BY key""".format(trip_id=trip_id))
		trip_timepoints = [k[1] for k in db.cursor.fetchall()]
		# print trip_timepoints
		db.select('timepoints',trip_id=trip_id)
		for i,s in enumerate(trip_stops):
			stop_id = s['stop_id']
			stop_seq = s['stop_sequence']
			stop = schedule.GetStop(stop_id)
			if i == 0:
				trip.AddStopTime(stop,stop_time='00:00:00')
			elif i == l-1:
				t = trip_timepoints.pop()
				trip.AddStopTime(stop,stop_time=t)
			elif s['is_timepoint']:
				t = trip_timepoints.pop(0)
				trip.AddStopTime(stop,stop_time=t)
			else:
				trip.AddStopTime(stop)


def fixTimes(t0,t1):
	t_0 = datetime.datetime.strptime(t0,'%H:%M')
	t_1 = datetime.datetime.strptime(t1,'%H:%M')
	if (t_1-t_0).total_seconds() > 0:
		end_time = t_1.strftime('%H:%M:%S')
	elif (t_1-t_0).total_seconds() < 0:
		str(t_1.hour+24)
		end_time = str(t_1.hour+24) + t_1.strftime(':%M:%S')
	start_time = t_0.strftime('%H:%M:%S')
	return start_time,end_time

def addFrequencies(db,schedule,debug=False):
	#f = transitfeed.Frequency({'trip_id':'C0.ida.H__','start_time':'00:00:00', 'end_time':'00:00:30', 'headway_secs':'345'})
	for t in schedule.GetTripList():
		trip_id = t.trip_id
		route_id = trip_id.split('.')[0]
		service = trip_id.split('.')[-1]
		diaLookup = {'H':'lav','S':'sabado','D':'domingo'}
		dia = diaLookup[service]
		for frec in db.select('servicios',route_id=route_id,dia=dia):
			start_time, end_time = fixTimes(frec['desde'],frec['hasta'])
			headway_secs = frec['frecuencia']*60
			#print start_time, end_time, headway_secs
			f = transitfeed.Frequency({'trip_id':trip_id, 
				'start_time':start_time, 
				'end_time':end_time, 
				'headway_secs':headway_secs})
			f.AddToSchedule(schedule)

def main():
	schedule = transitfeed.Schedule()
	db = o.dbInterface('dbRecorridos.sqlite')

	debug = False
	addAgencies(db, schedule, debug=debug)
	addServicePeriods(db, schedule, debug=debug)
	addCalendarDates(db, schedule, debug=debug)
	addStops(db, schedule, debug=debug)
	addShapes(db, schedule, debug=debug)
	addRoutes(db, schedule, debug=debug)
	addTrips(db, schedule, debug=debug)
	addStopTimes(db, schedule, debug=debug)
	addFrequencies(db, schedule, debug=debug)
	#accumulator = transitfeed.ProblemAccumulatorInterface()
	#reporter = transitfeed.ProblemReporter(accumulator)
	#schedule.Validate(reporter)
	schedule.Validate()
	schedule.WriteGoogleTransitFeed('google_transit.zip')
	db.close()

if __name__ == "__main__":

	#p = "/www/cartoar.com.ar/cgi-bin/virtual/lib/python2.7/site-packages/"
	#import sys
	#sys.path.append(p)


	main()
