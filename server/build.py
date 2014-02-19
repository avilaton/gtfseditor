#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division

import os
import zipfile
import codecs
import transitfeed
import datetime

import ormgeneric.ormgeneric as o
import gtfsdb
import util

class FeedFactory(object):
    """Turns dbRecorridos into a proper GTFS bundle"""
    def __init__(self, db, mode, debug):
        self.speed = 19
        self.db = db
        self.mode = mode
        self.debug = debug
        self.schedule = transitfeed.Schedule()

    def save(self, filename):
        """Save feed schedule to filename"""
        print("Saving feed to: "+ filename)

        self.schedule.WriteGoogleTransitFeed(filename)

    def build(self):
        """Build feed schedule from db"""
        print("Building schedule feed")

        self.loadAgencies()
        self.loadCalendar()
        self.loadCalendarDates()
        self.loadRoutes()
        if self.mode is 'frequency':
            self.loadTrips()
            self.loadStops()
            # self.loadUsedStops()
            self.loadStopTimes(interpolate=True)
            self.loadFrequencies()
        elif self.mode is 'initTimes':
            self.loadTripsInit()
            self.loadUsedStops()
            self.loadStopTimesInit()
        self.loadShapes()
        # self.loadFeedInfo()

    def validate(self):
        """Validate feed object"""
        print("Validating feed")
        # self.accumulator = CountingConsoleProblemAccumulator()
        # self.schedule.problem_reporter = transitfeed.ProblemReporter(self.accumulator)
        # accumulator = transitfeed.ProblemAccumulatorInterface()
        # reporter = transitfeed.ProblemReporter(accumulator)
        # self.schedule.Validate(reporter)
        self.schedule.Validate()

    def loadAgencies(self):
        print("Loading Agencies")
        for r in self.db.select('agency'):
            agency = self.schedule.AddAgency(r['agency_name'],r['agency_url'], 
                r['agency_timezone'],agency_id=r['agency_id'])
            agency.agency_phone = r['agency_phone']
            agency.agency_lang = r['agency_lang']
        self.schedule.SetDefaultAgency(self.schedule.GetAgencyList()[0])

    def loadCalendar(self):   
        print("Loading Calendar")
        for s in self.db.select('calendar'):
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
            self.schedule.AddServicePeriodObject(service)

    def loadCalendarDates(self):
        print("Loading Calendar Dates")
        """Inserts calendar date exceptions from calendar_dates table"""
        for feriado in self.db.select("calendar_dates"):
            service_period = self.schedule.GetServicePeriod(feriado['service_id'])
            if feriado['exception_type'] == "1":
                service_period.SetDateHasService(feriado['date'], has_service=True)
            elif feriado['exception_type'] == "2":
                service_period.SetDateHasService(feriado['date'], has_service=False)

    def loadRoutes(self):
        count = 0
        for route in self.db.select('routes'):
            route_id = route['route_id']
            if route_id not in ['C0'] and self.debug:
                continue
            if 'active' in dict(route) and not bool(route['active']):
                continue
            # print('adding route: ' + route_id)
            r = self.schedule.AddRoute(short_name=route['route_short_name'], 
                #long_name=route['route_long_name'], 
                long_name='', 
                route_id=route['route_id'],
                route_type=route['route_type'])
            r.agency_id = route['agency_id']
            r.route_color = route['route_color']
            r.route_text_color = route['route_text_color']
            count += 1
        print("Loaded "+ str(count) + "routes")

    def loadTrips(self):
        count = 0
        print("FIXME!!!")
        print("you have commented most services for debugging. remember to enable them")
        for r in self.schedule.GetRouteList():
            route_id = r['route_id']
            for t in self.db.select('trips', route_id=route_id):
                for service in self.schedule.GetServicePeriodList():
                    if service.service_id != 'H':
                        continue
                    trip_id = t['trip_id'] + '.' + service.service_id
                    trip = r.AddTrip(trip_id = trip_id,headsign=t['trip_headsign'])
                    trip.service_id = service.service_id
                    trip.shape_id = t['trip_id']
                    trip.direction_id = t['direction_id']
                    count += 1
        print("Loaded " + str(count) + " Trips")

    def loadStops(self):
        print("Loading Stops")
        # q = """SELECT DISTINCT stop_id FROM stop_seq 
        #   WHERE trip_id="{0}" OR trip_id="{1}" """.format('C0.ida','C0.vuelta')
        if self.debug:
            q = """SELECT * FROM stops WHERE stop_id IN 
                (SELECT DISTINCT stop_id FROM stop_seq 
                    WHERE trip_id='C0.ida')"""
        else:
            q = """SELECT * FROM stops WHERE stop_id IN 
                (SELECT DISTINCT stop_id FROM stop_seq)"""

        self.db.query(q)

        for s in self.db.cursor.fetchall():
            lat = s['stop_lat']
            lng = s['stop_lon']
            stop_id = str(s['stop_id'])
            stop = self.schedule.AddStop(lat=float(lat),lng=float(lng),name=s['stop_name'],stop_id=stop_id)
            stop.stop_code = s['stop_id']

    def loadShapes(self):
        print("Loading Shapes")
        self.db.query("""SELECT DISTINCT shape_id FROM shapes""")

        usedShapes = set([trip['shape_id'] for trip in self.schedule.GetTripList()])

        for shape_id in usedShapes:
            self.db.query("""SELECT * FROM shapes WHERE shape_id="{0}" ORDER BY shape_pt_sequence""".format(shape_id))
            l = {'shape_pt_lat':0,'shape_pt_lon':0}
            shapeObject = transitfeed.Shape(shape_id=shape_id)
            for pt in self.db.cursor.fetchall():
                shapeObject.AddPoint(lat=pt['shape_pt_lat'],lon=pt['shape_pt_lon'])
            self.schedule.AddShapeObject(shapeObject)

    def loadStopTimes(self, interpolate=True):
        """Adding Stop Times"""
        print("Loading Stop Times")
        #interpolate = False
        for trip in self.schedule.GetTripList():
            trip_id = trip['trip_id'][:-2]
            trip_stops = self.getTripStops(trip_id)
            l = len(trip_stops)

            total_distance = float(trip_stops[-1]["shape_dist_traveled"])
            # print(trip_id + " has " + str(total_distance) + " km")

            # old total time computation
            # trip_timepoints = self.gettimepoints(trip_id)
            # total_time = util.hhmmss2sec(trip_timepoints[-1])
            
            # new total time computation
            speed = self.speed # km/h
            total_time = 3600*total_distance/speed # seconds
            # print "total time for", trip_id, " is: ", util.sec2hhmmss(total_time), "distance: ", total_distance

            for i,s in enumerate(trip_stops):
                stop_id = s['stop_id']
                traveled = float(s['shape_dist_traveled'])
                stop = self.schedule.GetStop(stop_id)
                # stop_seq = s['stop_sequence']
                if interpolate:
                    t = int(total_time*traveled/(total_distance))
                    # print t, util.sec2hhmmss(t)
                    trip.AddStopTime(stop,stop_time=util.sec2hhmmss(t))
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

    def loadFrequencies(self):
        """ A Frequency object is created using
            f = transitfeed.Frequency({'trip_id':'C0.ida.H__', 
                'start_time':'00:00:00', 
                'end_time':'00:00:30', 
                'headway_secs':'345'})
        """
        print("Loading Frecuencies")
        for t in self.schedule.GetTripList():
            trip_id = t.trip_id
            for row in self.db.select('services', route_id=t.route_id, 
                service_id=t.service_id):
                start_time, end_time = util.fixTimes(row['start_time'],row['end_time'])
                headway_secs = row['headway_secs']
                f = transitfeed.Frequency({'trip_id':trip_id, 
                    'start_time':start_time, 
                    'end_time':end_time, 
                    'headway_secs':headway_secs})
                f.AddToSchedule(self.schedule)

    def loadTripsInit(self):
        for r in self.schedule.GetRouteList():
            route_id = r['route_id']
            for t in self.db.select('trips', route_id=route_id):
                if t['trip_id'] != 'C0.ida' and self.debug:
                    continue
                for service in self.schedule.GetServicePeriodList():
                    for init_time in self.getTripInitTimes(db, t['trip_id'], service.service_id):
                        trip_id = t['trip_id'] + '.' + service.service_id + '.' + str(init_time)
                        trip = r.AddTrip(trip_id = trip_id,headsign=t['trip_headsign'])
                        trip.service_id = service.service_id
                        trip.shape_id = t['trip_id']
                        trip.direction_id = t['direction_id']

    def loadUsedStops(self):
        tripIds = set([])
        for r in self.schedule.GetRouteList():
            route_id = r['route_id']
            for trip in self.db.select('trips', route_id=route_id):
                tripIds.add(trip['trip_id'])

        usedStopIds = set([])
        for trip_id in tripIds:
            for stop in self.db.select('stop_seq', trip_id=trip_id):
                usedStopIds.add(stop['stop_id'])
        
        for stop_id in usedStopIds:
            s = self.db.select('stops', stop_id=stop_id)[0]
            lat = s['stop_lat']
            lng = s['stop_lon']
            stop_id = s['stop_id']
            stop = self.schedule.AddStop(lat=float(lat),lng=float(lng),name=s['stop_name'],stop_id=stop_id)
            stop.stop_code = s['stop_id']

    def loadFeedInfo(self):
        pass

    def getTripInitTimes(self, trip_id, service_period):
        # fetch init times
        self.db.query("""SELECT {service_period} FROM salidas 
            WHERE trip_id={trip_id} ORDER BY {service_period}""".format(
                trip_id=trip_id,
                service_period=service_period))
        init_times = []
        for r in self.db.cursor.fetchall():
            if r[0]:
                init_times.append(util.hhmmss2sec(r[0]))
        return init_times

    def getTripStopSeq(self, trip_id):
        q = """SELECT * FROM stop_seq 
            WHERE trip_id="{0}" 
            ORDER BY stop_sequence""".format(trip_id)
        self.db.query(q)
        trip_stops = self.db.cursor.fetchall()
        return trip_stops

    def loadStopTimesInit(self):
        """Adding Stop Times from trip start times"""

        for trip in self.schedule.GetTripList():
            trip_id, service_id, init_time = trip['trip_id'].split('.')
            print(trip['trip_id'])
            init_times = self.getTripInitTimes(db, trip_id, service_id)
            trip_stops = self.getTripStopSeq(db, trip_id)

            previousTime = None
            for s in trip_stops:
                stop_id = s['stop_id']
                stop = self.schedule.GetStop(stop_id)
                t = util.hhmmss2sec(s['time']) + int(init_time)
                stop_time = util.sec2hhmmss(t)
                # print(stop_id + ' at time ' + stop_time)
                if not previousTime:
                    trip.AddStopTime(stop,stop_time=stop_time)
                elif previousTime and (previousTime < util.hhmmss2sec(stop_time)):
                    trip.AddStopTime(stop,stop_time=stop_time)
                else:
                    trip.AddStopTime(stop)
                previousTime = util.hhmmss2sec(stop_time)
            previousTime = None

    def gettimepoints(self, trip_id):
        trip_id = trip_id.replace('V0.','V0H.')
        trip_id = trip_id.replace('N3.Almacenero.','N3.')
        trip_id = trip_id.replace('N3.Warcalde.','N3.')
        self.db.query("""SELECT key,value FROM timepoints 
            WHERE trip_id='{trip_id}' ORDER BY key""".format(trip_id=trip_id))
        return [k[1] for k in self.db.cursor.fetchall()]

    def getTripStops(self, trip_id):
        q = """SELECT * FROM stop_seq 
                WHERE trip_id="{0}" 
            ORDER BY stop_sequence""".format(trip_id)
        self.db.query(q)
        trip_stops = self.db.cursor.fetchall()
        return trip_stops

######################################33
# Feed info utils
def addFeedInfo(schedule):
    feedInfo = transitfeed.FeedInfo()
    feedInfo.feed_publisher_url = 'http://www.cordoba.gov.ar/'
    feedInfo.feed_publisher_name = u'Municipalidad de Córdoba'
    feedInfo.feed_lang = 'es'
    feedInfo.feed_version = '0.2'

    schedule.AddFeedInfoObject(feedInfo)

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

def attachFeedInfo(filename):
    with zipfile.ZipFile(filename, "a") as z:
        z.write('database/feed_info.txt', 'feed_info.txt')

def extract(filename):
    """extract for debuging"""
    with zipfile.ZipFile(filename, "r") as z:
        if not os.path.exists('extracted/'):
            os.makedirs('extracted/')
        for filename in z.namelist():
            with file('extracted/'+filename, "w") as outfile:
                outfile.write(z.read(filename))

def precompilationTasks(db):
    """ These tasks build computed data into the DB from the 
        existing rows """

    toolbox = gtfsdb.toolbox(db)
    # toolbox.constructStopNames()
    trips = toolbox.allTrips()
    for trip_id in trips:
        print("sorting trip: "+trip_id)
        toolbox.sortTripStops(trip_id)
    toolbox.commit()
    toolbox.updateDistTraveled()
    toolbox.commit()

def compilationTasks(db):
    DEBUG = False

    feed = FeedFactory(db, mode='frequency', debug=DEBUG)
    feed.build()
    feed.save('compiled/google_transit.zip')
    attachFeedInfo('compiled/google_transit.zip')
    feed.validate()
    extract('compiled/google_transit.zip')

def main():
    import config

    db = o.dbInterface(config.DATABASE)

    precompilationTasks(db)
    compilationTasks(db)

    db.close()

if __name__ == "__main__":
    main()

