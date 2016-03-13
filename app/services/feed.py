#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import csv
import resource
import transitfeed
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
import zipfile
import shutil

from app import db
from ..models import *
from ..services.stop_times import offset_sequence_times
from ..services import defaults

class Feed(object):
  """GTFS schedule feed factory"""
  def __init__(self, filename='google_transit.zip', db=db):
    self.db = db
    self.filename = filename
    self.fileObj = StringIO()
    self.trip_start_times_default = None
    self.schedule = transitfeed.Schedule(memory_db=False)

  def __repr__(self):
    return 'GTFS feed:' + self.filename

  def build(self):
    logger.info("Feed build started")

    self.loadAgencies()
    self.loadCalendar()
    self.loadCalendarDates()
    self.loadStops()
    self.loadRoutes()
    self.loadShapes()

    # self.loadAllFrequencies()

    self.schedule.WriteGoogleTransitFeed(self.fileObj)
    self.loadFeedInfo()
    logger.info("Feed build completed")
    return self.fileObj

  def saveTo(self, directory):
    self.fileObj.seek(0)
    with open(directory + self.filename, 'w') as outfile:
      shutil.copyfileobj(self.fileObj, outfile)

  def validate(self):
    """Validate feed object"""
    logger.info("Validating feed")
    # self.accumulator = CountingConsoleProblemAccumulator()
    # self.schedule.problem_reporter = transitfeed.ProblemReporter(self.accumulator)
    # accumulator = transitfeed.ProblemAccumulatorInterface()
    # reporter = transitfeed.ProblemReporter(accumulator)
    # self.schedule.Validate(reporter)
    self.schedule.Validate()

  def loadAgencies(self):
    logger.info("Loading Agencies")

    for row in self.db.query(Agency).all():
      agency = self.schedule.AddAgency(row.agency_name, row.agency_url, 
          row.agency_timezone or "", agency_id=row.agency_id)
      agency.agency_phone = row.agency_phone
      agency.agency_lang = row.agency_lang or ""
    if len(self.schedule.GetAgencyList()):
      self.schedule.SetDefaultAgency(self.schedule.GetAgencyList()[0])

  def loadCalendar(self):
    logger.info("Loading Calendar")
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
      'sunday']
    for s in self.db.query(Calendar).all():
      service = transitfeed.ServicePeriod()
      service.SetServiceId(s.service_id)
      service.SetStartDate(str(s.start_date))
      service.SetEndDate(str(s.end_date))
      for i, day in enumerate(days):
        hasService = bool(int(getattr(s, day)))
        service.SetDayOfWeekHasService(i, hasService)
      self.schedule.AddServicePeriodObject(service)

  def loadCalendarDates(self):
    """Inserts calendar date exceptions from calendar_dates table"""
    logger.info("Loading Calendar Dates")

    exceptions = {"1": True, "2": False}

    for date in self.db.query(CalendarDate).all():
      service_period = self.schedule.GetServicePeriod(date.service_id)
      service_period.SetDateHasService(date.date, has_service=exceptions[date.exception_type])

  def loadRoutes(self):
    """Loads active routes into schedule"""
    logger.info("Loading Routes")
    routes = self.db.query(Route).order_by(Route.route_short_name).filter(Route.active).all()
    count = len(routes)

    for i, row in enumerate(routes):
      route_id = row.route_id

      mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
      logger.info("Loading {1}/{2} ({3}), route_short_name: {0}, mode: {4}".format(
                    row.route_short_name,
                    i,
                    count,
                    mem,
                    row.build_type))

      route = self.schedule.AddRoute(short_name=row.route_short_name,
          long_name=row.route_long_name or "",
          route_id=row.route_id,
          route_type=row.route_type)
      route.agency_id = row.agency_id
      route.route_color = row.route_color
      route.route_text_color = row.route_text_color

      if row.build_type in ['initial_times']:
        self.loadTripsByInitialTimes(route)
      elif row.build_type in ['frequency']:
        self.loadTripsByFrequency(route)
      else:
        raise NotImplementedError

  def loadTripsByFrequency(self, route):
    """Loads active trips by frequency"""

    for tripRow in self.db.query(Trip).filter_by(route_id=route.route_id)\
                                      .filter(Trip.active)\
                                      .order_by(Trip.trip_id):
      services = self.schedule.GetServicePeriodList()
      for service in services:
        trip_id = '.'.join([
                            str(route.route_id),
                            str(tripRow.trip_id),
                            str(service.service_id)
                          ])
        trip = route.AddTrip(trip_id = trip_id, headsign=tripRow.trip_headsign)
        trip.service_id = service.service_id
        trip.shape_id = tripRow.shape_id
        trip.direction_id = tripRow.direction_id

        self.loadTripRouteFrequencies(trip)
        self.loadStopTimesByFrequency(trip)

  def loadTripsByInitialTimes(self, route):
    """Loads active trips into schedule"""

    for tripRow in self.db.query(Trip).filter_by(route_id=route.route_id)\
                                      .filter(Trip.active)\
                                      .order_by(Trip.trip_id):

      trip_start_times = self.db.query(TripStartTime).filter_by(trip_id=tripRow.trip_id).all()
      if not trip_start_times:
        self.loadDefaultTripStartTimes()
        trip_start_times = self.trip_start_times_default

      stop_sequence = self.db.query(StopSeq).filter_by(trip_id=tripRow.trip_id).\
        order_by(StopSeq.stop_sequence).all()

      for startTimeRow in trip_start_times:
        new_trip_id = '.'.join(map(str, [route.route_short_name,
                                         tripRow.card_code,
                                         tripRow.trip_id,
                                         startTimeRow.service_id,
                                         startTimeRow.start_time
                                        ]))
        trip = route.AddTrip(trip_id = new_trip_id, headsign=tripRow.trip_headsign)
        trip.service_id = startTimeRow.service_id
        trip.shape_id = tripRow.shape_id
        trip.direction_id = tripRow.direction_id

        self.loadStopTimesByInitialTimes(trip, tripRow.trip_id, startTimeRow, stop_sequence=stop_sequence)

  def loadDefaultTripStartTimes(self):
    if self.trip_start_times_default:
      return
    self.trip_start_times_default = [item for item in defaults.startTimes()]
    logger.info("Loading Default Calendar")
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 
      'sunday']

    service = transitfeed.ServicePeriod()
    service.SetServiceId('default')
    service.SetStartDate('20150101')
    service.SetEndDate('20151201')
    for i, day in enumerate(days):
      service.SetDayOfWeekHasService(i, True)
    self.schedule.AddServicePeriodObject(service)

  def loadStops(self):
    logger.info("Loading Stops")
    active_routes_subq = self.db.query(Route.route_id).filter(Route.active).subquery()
    active_trips_subq = self.db.query(Trip.trip_id).\
      filter(Trip.route_id.in_(active_routes_subq), Trip.active).subquery()
    used_stops_subq = self.db.query(StopSeq.stop_id).distinct().\
      filter(StopSeq.trip_id.in_(active_trips_subq)).subquery()
    stops_query = self.db.query(Stop).filter(Stop.stop_id.in_(used_stops_subq))

    for stop in stops_query.all():
      lat = stop.stop_lat
      lng = stop.stop_lon
      stop_id = stop.stop_id
      stopObj = self.schedule.AddStop(lat=float(lat), lng=float(lng),
        name=stop.stop_name, stop_id=str(stop.stop_id))
      stopObj.stop_code = stop.stop_code

  def loadStopTimesByFrequency(self, trip):
    """Adding Stop Times from trip start times"""

    # Should use StopTimesFactory instead of reading from stop_times table.
    trip_id = trip.trip_id.split('.')[1]

    for stopTime in self.db.query(StopSeq).filter_by(trip_id=trip_id).\
      order_by(StopSeq.stop_sequence).all():
      stop = self.schedule.GetStop(str(stopTime.stop_id))
      stop_time = stopTime.stop_time
      if stop_time:
        try:
          trip.AddStopTime(stop, stop_time=stop_time)
        except Exception, e:
          trip.AddStopTime(stop)
          logger.error(e)
      else:
        trip.AddStopTime(stop)

  def loadStopTimesByInitialTimes(self, trip, seq_trip_id, startTimeRow, stop_sequence):
    """Adding Stop Times from trip start times"""
    # logger.info("Loading Stop Times for stop_seq:{0}, trip_id:{1}".format(seq_trip_id, trip.trip_id))

    for stop_time in offset_sequence_times(stop_sequence, startTimeRow.start_time):
      stop = self.schedule.GetStop(str(stop_time['stop_id']))
      arrival_time = stop_time['arrival_time']
      if arrival_time:
        try:
          trip.AddStopTime(stop, stop_time=arrival_time)
        except Exception, e:
          trip.AddStopTime(stop)
          logger.error(e)
      else:
        trip.AddStopTime(stop)

  def loadShapes(self):
    logger.info("Loading Shapes")

    usedShapes = set([trip['shape_id'] for trip in self.schedule.GetTripList()])

    for shape_id in usedShapes:
      shape_obj = self.db.query(ShapePath).filter_by(shape_id=shape_id).first()
      shape_path = shape_obj.shape_path_array
      shape = transitfeed.Shape(shape_id=shape_id)
      for pt in shape_path:
        shape.AddPoint(lon=pt[0], lat=pt[1])
      self.schedule.AddShapeObject(shape)

  def loadTripRouteFrequencies(self, trip):
      logger.info("Loading trip route Frequencies")

      services = self.db.query(RouteFrequency).filter_by(route_id=trip.route_id, 
        service_id=trip.service_id).all()
      for route_service in services:
        f = transitfeed.Frequency({'trip_id': trip.trip_id,
            'start_time': route_service.start_time,
            'end_time': route_service.end_time,
            'headway_secs': route_service.headway_secs})
        f.AddToSchedule(self.schedule)

  def loadAllFrequencies(self):
      logger.info("Loading Frequencies")
      for freq in self.db.query(Frequency).all():
        f = transitfeed.Frequency({'trip_id':freq.trip_id, 
            'start_time':freq.start_time, 
            'end_time':freq.end_time, 
            'headway_secs':freq.headway_secs})
        f.AddToSchedule(self.schedule)

  def loadFeedInfo(self):
    logger.info("Load Feed Info")

    keys = ['feed_publisher_name', 'feed_start_date', 'feed_version', 
        'feed_end_date', 'feed_lang', 'feed_publisher_url']
    feed_info_txt = StringIO()
    writer = csv.DictWriter(feed_info_txt, keys)
    writer.writeheader()
    for info in self.db.query(FeedInfo).all():
      uDict = {k:v.encode('utf-8') for k, v in info.to_json.iteritems() if v}
      writer.writerow(uDict)
    with zipfile.ZipFile(self.fileObj, "a", zipfile.ZIP_DEFLATED) as feed_file:
      feed_file.writestr('feed_info.txt', feed_info_txt.getvalue())
