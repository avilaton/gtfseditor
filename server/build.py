#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division

import os
import zipfile
import codecs

import transitfeed
import datetime
import ormgeneric.ormgeneric as o
import gtfstools


FEED_START_DATE = '20130401'
FEED_END_DATE = '20131231'

class Schedule(object):
    """Turns dbRecorridos into a proper GTFS bundle"""
    def __init__(self, db, debug):
        # super(Schedule, self).__init__()
        self.db = db
        self.debug = debug
        self.schedule = transitfeed.Schedule()

    def loadAgencies(self):
        for r in self.db.select('agency'):
            agency = self.schedule.AddAgency(r['agency_name'],r['agency_url'], 
                r['agency_timezone'],agency_id=r['agency_id'])
            agency.agency_phone = r['agency_phone']
            agency.agency_lang = r['agency_lang']
        self.schedule.SetDefaultAgency(self.schedule.GetAgencyList()[0])


def addAgencies(db,schedule,debug=False):
    for r in db.select('agency'):
        agency = schedule.AddAgency(r['agency_name'],r['agency_url'],r['agency_timezone'],agency_id=r['agency_id'])
        agency.agency_phone = r['agency_phone']
        agency.agency_lang = r['agency_lang']
    schedule.SetDefaultAgency(schedule.GetAgencyList()[0])

def addRoutes(db,schedule,debug=False):
    for route in db.select('routes'):
        route_id = route['route_id']
        if route_id not in ['C0'] and debug:
            continue
        if 'active' in dict(route) and not bool(route['active']):
            continue
        print('adding route: ' + route_id)
        r = schedule.AddRoute(short_name=route['route_short_name'], 
            #long_name=route['route_long_name'], 
            long_name='', 
            route_id=route['route_id'],
            route_type=route['route_type'])
        r.agency_id = route['agency_id']
        r.route_color = route['route_color']
        r.route_text_color = route['route_text_color']

def addCalendar(db,schedule,debug=False):   
    for s in db.select('calendar'):
        service = transitfeed.ServicePeriod()
        service.SetServiceId(s['service_id'])
        service.SetStartDate(str(s['start_date']))
        service.SetEndDate(str(s['end_date']))
        service.SetDayOfWeekHasService(0, bool(s['monday']) )
        service.SetDayOfWeekHasService(1, bool(s['tuesday']) )
        service.SetDayOfWeekHasService(2, bool(s['wednesday']) )
        service.SetDayOfWeekHasService(3, bool(s['thursday']) )
        service.SetDayOfWeekHasService(4, bool(s['friday']) )
        service.SetDayOfWeekHasService(5, bool(s['saturday']) )
        service.SetDayOfWeekHasService(6, bool(s['sunday']) )
        schedule.AddServicePeriodObject(service)

def addCalendarDates(db, schedule, debug=False):
    """Inserts calendar date exceptions from calendar_dates table"""

    for feriado in db.select("calendar_dates"):
        service_period = schedule.GetServicePeriod(feriado['service_id'])
        if feriado['exception_type'] == "1":
            service_period.SetDateHasService(feriado['date'], has_service=True)
        elif feriado['exception_type'] == "2":
            service_period.SetDateHasService(feriado['date'], has_service=False)
            
def addUsedStops(db, schedule, debug=False):
    tripIds = set([])
    for r in schedule.GetRouteList():
        route_id = r['route_id']
        for trip in db.select('trips', route_id=route_id):
            tripIds.add(trip['trip_id'])

    usedStopIds = set([])
    for trip_id in tripIds:
        for stop in db.select('stop_seq', trip_id=trip_id):
            usedStopIds.add(stop['stop_id'])
    
    for stop_id in usedStopIds:
        s = db.select('stops', stop_id=stop_id)[0]
        lat = s['stop_lat']
        lng = s['stop_lon']
        stop_id = s['stop_id']
        stop = schedule.AddStop(lat=float(lat),lng=float(lng),name=s['stop_name'],stop_id=stop_id)
        stop.stop_code = s['stop_id']

def addStops(db,schedule,debug=False):
    # q = """SELECT DISTINCT stop_id FROM stop_seq 
    #   WHERE trip_id="{0}" OR trip_id="{1}" """.format('C0.ida','C0.vuelta')
    if debug:
        q = """SELECT * FROM stops WHERE stop_id IN 
            (SELECT DISTINCT stop_id FROM stop_seq 
                WHERE trip_id='C0.ida')"""
    else:
        q = """SELECT * FROM stops WHERE stop_id IN 
            (SELECT DISTINCT stop_id FROM stop_seq)"""
    
    db.query(q)

    for s in db.cursor.fetchall():
        lat = s['stop_lat']
        lng = s['stop_lon']
        stop_id = s['stop_id']
        stop = schedule.AddStop(lat=float(lat),lng=float(lng),name=s['stop_name'],stop_id=stop_id)
        stop.stop_code = s['stop_id']

def addShapes(db,schedule,debug=False):
    db.query("""SELECT DISTINCT shape_id FROM shapes""")

    usedShapes = set([trip['shape_id'] for trip in schedule.GetTripList()])

    for shape_id in usedShapes:
        db.query("""SELECT * FROM shapes WHERE shape_id="{0}" ORDER BY shape_pt_sequence""".format(shape_id))
        l = {'shape_pt_lat':0,'shape_pt_lon':0}
        shapeObject = transitfeed.Shape(shape_id=shape_id)
        for pt in db.cursor.fetchall():
            shapeObject.AddPoint(lat=pt['shape_pt_lat'],lon=pt['shape_pt_lon'])
        schedule.AddShapeObject(shapeObject)


def addTrips(db,schedule,debug=False):
    for r in schedule.GetRouteList():
        route_id = r['route_id']
        for t in db.select('trips', route_id=route_id):
            if t['trip_id'] != 'C0.ida' and debug:
                continue
            for service in schedule.GetServicePeriodList():
                trip_id = t['trip_id'] + '.' + service.service_id
                trip = r.AddTrip(trip_id = trip_id,headsign=t['trip_headsign'])
                trip.service_id = service.service_id
                trip.shape_id = t['trip_id']
                trip.direction_id = t['direction_id']


def addTripsInit(db,schedule,debug=False):
    for r in schedule.GetRouteList():
        route_id = r['route_id']
        for t in db.select('trips', route_id=route_id):
            if t['trip_id'] != 'C0.ida' and debug:
                continue
            for service in schedule.GetServicePeriodList():
                for init_time in getTripInitTimes(db, t['trip_id'], service.service_id):
                    trip_id = t['trip_id'] + '.' + service.service_id + '.' + str(init_time)
                    trip = r.AddTrip(trip_id = trip_id,headsign=t['trip_headsign'])
                    trip.service_id = service.service_id
                    trip.shape_id = t['trip_id']
                    trip.direction_id = t['direction_id']


def getTripInitTimes(db, trip_id, service_period):
    # fetch init times
    db.query("""SELECT {service_period} FROM salidas 
        WHERE trip_id={trip_id} ORDER BY {service_period}""".format(
            trip_id=trip_id,
            service_period=service_period))
    init_times = []
    for r in db.cursor.fetchall():
        if r[0]:
            init_times.append(hhmmss2sec(r[0]))
    return init_times

def getTripStopSeq(db, trip_id):
    q = """SELECT * FROM stop_seq 
        WHERE trip_id="{0}" 
        ORDER BY stop_sequence""".format(trip_id)
    db.query(q)
    trip_stops = db.cursor.fetchall()
    return trip_stops

def addStopTimesInit(db, schedule, debug=False):
    """Adding Stop Times from trip start times"""

    for trip in schedule.GetTripList():
        trip_id, service_id, init_time = trip['trip_id'].split('.')
        print(trip['trip_id'])
        init_times = getTripInitTimes(db, trip_id, service_id)
        trip_stops = getTripStopSeq(db, trip_id)

        previousTime = None
        for s in trip_stops:
            stop_id = s['stop_id']
            stop = schedule.GetStop(stop_id)
            t = hhmmss2sec(s['time']) + int(init_time)
            stop_time = sec2hhmmss(t)
            # print(stop_id + ' at time ' + stop_time)
            if not previousTime:
                trip.AddStopTime(stop,stop_time=stop_time)
            elif previousTime and (previousTime < hhmmss2sec(stop_time)):
                trip.AddStopTime(stop,stop_time=stop_time)
            else:
                trip.AddStopTime(stop)
            previousTime = hhmmss2sec(stop_time)
        previousTime = None


def addStopTimes(db,schedule,interpolate=True, debug=False):
    """Adding Stop Times"""
    #interpolate = False
    for trip in schedule.GetTripList():
        trip_id = trip['trip_id'][:-2]
        # print trip_id

        q = """SELECT * FROM stop_seq 
            WHERE trip_id="{0}" 
            ORDER BY stop_sequence""".format(trip_id)
        db.query(q)
        trip_stops = db.cursor.fetchall()
        l = len(trip_stops)

        total_distance = float(trip_stops[-1]["shape_dist_traveled"])

        trip_timepoints = gettimepoints(db, trip_id)
        # print trip_timepoints
        total_time = hhmmss2sec(trip_timepoints[-1])
        # print "total time for", trip_id, " is: ", sec2hhmmss(total_time), "distance: ", total_distance

        for i,s in enumerate(trip_stops):
            stop_id = s['stop_id']
            traveled = float(s['shape_dist_traveled'])
            stop = schedule.GetStop(stop_id)
            # stop_seq = s['stop_sequence']
            if interpolate:
                t = int(total_time*traveled/(total_distance))
                # print t, sec2hhmmss(t)
                trip.AddStopTime(stop,stop_time=sec2hhmmss(t))
            else:
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

def gettimepoints(db, trip_id):
    trip_id = trip_id.replace('V0.','V0H.')
    trip_id = trip_id.replace('N3.Almacenero.','N3.')
    trip_id = trip_id.replace('N3.Warcalde.','N3.')
    db.query("""SELECT key,value FROM timepoints 
        WHERE trip_id='{trip_id}' ORDER BY key""".format(trip_id=trip_id))
    return [k[1] for k in db.cursor.fetchall()]

def sec2hhmmss(sec):
    seconds = sec%60
    
    sec = sec-seconds
    min = int(sec/60)

    minutes = min%60    
    h = min-minutes
    hours = int(h/60)
    t = map(lambda d:"{0:02d}".format(d), [hours, minutes, seconds])
    formatedTime = ':'.join(t)

    return formatedTime

def hhmmss2sec(hhmmss):
    # hms = datetime.datetime.strptime(hhmmss,'%H:%M:%S')
    h,m,s = map(lambda x:int(x), hhmmss.split(':'))
    return h*60*60+m*60+s

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
        route_id = t.route_id
        # route_id = trip_id.split('.')[0]
        # service = trip_id.split('.')[-1]
        service_id = t.service_id
        diaLookup = {'H':'lav','S':'sabado','D':'domingo'}
        dia = diaLookup[service_id]
        for frec in db.select('servicios',route_id=route_id,dia=dia):
            start_time, end_time = fixTimes(frec['desde'],frec['hasta'])
            headway_secs = frec['frecuencia']*60
            #print start_time, end_time, headway_secs
            f = transitfeed.Frequency({'trip_id':trip_id, 
                'start_time':start_time, 
                'end_time':end_time, 
                'headway_secs':headway_secs})
            f.AddToSchedule(schedule)

def addFeedInfo(schedule):
    feedInfo = transitfeed.FeedInfo()
    feedInfo.feed_publisher_url = 'http://www.cordoba.gov.ar/'
    feedInfo.feed_publisher_name = u'Municipalidad de Córdoba'
    feedInfo.feed_lang = 'es'
    feedInfo.feed_version = '0.2'

    schedule.AddFeedInfoObject(feedInfo)

def updateDistTraveled(db):
    db.query("""SELECT DISTINCT trip_id FROM stop_seq""")
    for row in db.cursor.fetchall():
        trip_id = row["trip_id"]
        tripTb = gtfstools.Trip(db, trip_id)
        tripTb.computeAllSnaps()
        for s in tripTb.snaps:
            stop_id = s[0]['stop_id']
            d = "{0:.3f}".format(s[1]['traveled'])
            print stop_id, d
            q = """UPDATE stop_seq SET shape_dist_traveled='{d}' 
                WHERE trip_id='{trip_id}' 
                AND stop_id='{stop_id}'""".format(d=d, trip_id=trip_id, stop_id=stop_id)
            db.query(q)

def createFeedInfoFile(db, debug):
    import csv

    keys = ['feed_publisher_name', 'feed_start_date', 'feed_version', 
        'feed_end_date', 'feed_lang', 'feed_publisher_url']
    with open('database/feed_info_test.txt', 'w') as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        rows = []
        rows = [dict(r) for r in db.select('feed_info')]
        for r in rows:
            row = dict((k, v.encode('utf-8')) for k, v in r.iteritems())
            writer.writerow(row)

def constructStopNames(db):
    db.query("""SELECT * FROM stops WHERE stop_id IN 
        (SELECT DISTINCT stop_id FROM stop_seq)""")

    for stop in db.cursor.fetchall():
        lat = stop['stop_lat']
        lng = stop['stop_lon']
        if stop['stop_calle']:
            if stop['stop_numero']:
                name = stop['stop_calle'] + ' ' + str(stop['stop_numero'])
            else:
                if stop['stop_entre']:
                    if ' y ' in stop['stop_entre']:
                        name = stop['stop_calle'] + u' entre ' + stop['stop_entre']
                    else:
                        name = stop['stop_calle'] + u', ' + stop['stop_entre']
                else:
                    name = stop['stop_calle']
        else:
            name = stop['stop_id']
        # print name
        db.query("""UPDATE stops SET stop_name='{name}' 
            WHERE stop_id='{stop_id}' """.format(name=name.encode('utf-8'), stop_id=stop['stop_id']))

def buildSchedule(db, debug, mode):
    schedule = transitfeed.Schedule()
    
    addAgencies(db, schedule, debug)
    addCalendar(db, schedule, debug)
    addCalendarDates(db, schedule, debug)
    addRoutes(db, schedule, debug)
    if mode is 'frequency':
        addTrips(db, schedule, debug)
        addStops(db, schedule, debug)
        addShapes(db, schedule, debug)
        addStopTimes(db, schedule, interpolate=True, debug=debug)
        addFrequencies(db, schedule, debug)
    elif mode is 'initTimes':
        addTripsInit(db, schedule, debug)
        addUsedStops(db, schedule, debug)
        addShapes(db, schedule, debug)
        addStopTimesInit(db, schedule, debug)

    addFeedInfo(schedule)
        
    return schedule


def attachFeedInfo():
    # createFeedInfoFile(db, debug=DEBUG)
    # add feed info
    with zipfile.ZipFile('compiled/google_transit.zip', "a") as z:
        z.write('database/feed_info.txt', 'feed_info.txt')

    
    #extract for debuging

    with zipfile.ZipFile('compiled/google_transit.zip', "r") as z:
        if not os.path.exists('extracted/'):
            os.makedirs('extracted/')
        for filename in z.namelist():
            with file('extracted/'+filename, "w") as outfile:
                outfile.write(z.read(filename))

def validateAndSaveSchedule(schedule):
    #accumulator = transitfeed.ProblemAccumulatorInterface()
    #reporter = transitfeed.ProblemReporter(accumulator)
    #schedule.Validate(reporter)
    schedule.Validate()
    schedule.WriteGoogleTransitFeed('compiled/google_transit.zip')

    attachFeedInfo()

def main():
    DEBUG = False

    db = o.dbInterface('database/dbRecorridos.sqlite')

    # myFeed = Schedule(db, debug=DEBUG)
    # myFeed.loadAgencies()
    # myFeed.loadCalendar()
    # updateDistTraveled(db)

    constructStopNames(db)

    # schedule = buildSchedule(db, DEBUG, mode='frequency')
    schedule = buildSchedule(db, DEBUG, mode='initTimes')

    db.close()

    validateAndSaveSchedule(schedule)
    


if __name__ == "__main__":
    main()

    #p = "/www/cartoar.com.ar/cgi-bin/virtual/lib/python2.7/site-packages/"
    #import sys
    #sys.path.append(p)

