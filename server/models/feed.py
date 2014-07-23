#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import csv
import transitfeed
import StringIO
import zipfile

from server import engine
from server.models import Route
from server.models import Agency
from server.models import Trip
from server.models import Calendar
from server.models import CalendarDate
from server.models import Shape
from server.models import Frequency
from server.models import FeedInfo
from server.models import Stop
from server.models import StopSeq
from server.models import StopTime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

Session = sessionmaker(bind=engine)
db = scoped_session(Session)

class Feed(object):
  """GTFS schedule feed factory"""
  def __init__(self, filename):
    self.filename = filename
    self.schedule = transitfeed.Schedule()

  def __repr__(self):
    return 'GTFS feed at:' + self.filename

  def build(self):
    logger.info("Feed build started")
    self.loadAgencies()
    self.loadCalendar()
    self.loadCalendarDates()
    self.loadRoutes()
    self.loadTrips()
    self.loadStops()
    self.loadStopTimes()
    self.loadShapes()
    self.loadFrequencies()
    self.schedule.WriteGoogleTransitFeed(self.filename)
    self.loadFeedInfo()
    logger.info("Feed build completed")

  def loadAgencies(self):
    logger.info("Loading Agencies")

    for row in db.query(Agency).all():
      agency = self.schedule.AddAgency(row.agency_name, row.agency_url, 
          row.agency_timezone, agency_id=row.agency_id)
      agency.agency_phone = row.agency_phone
      agency.agency_lang = row.agency_lang
    if len(self.schedule.GetAgencyList()):
      self.schedule.SetDefaultAgency(self.schedule.GetAgencyList()[0])

  def loadCalendar(self):
    logger.info("Loading Calendar")
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 
      'sunday']
    for s in db.query(Calendar).all():
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

    for date in db.query(CalendarDate).all():
      service_period = self.schedule.GetServicePeriod(date.service_id)
      service_period.SetDateHasService(date.date, has_service=exceptions[date.exception_type])

  def loadRoutes(self):
    """Loads active routes into schedule"""
    logger.info("Loading Routes")

    for route in db.query(Route).all():
      route_id = route.route_id
      # if str(route.active) is not "TRUE":
      #   continue
      logger.info("Loading route_id: {0}".format(route_id))
      r = self.schedule.AddRoute(short_name=route.route_short_name, 
          #long_name=route.route_long_name, 
          long_name='', 
          route_id=route.route_id,
          route_type=route.route_type)
      r.agency_id = route.agency_id
      r.route_color = route.route_color
      r.route_text_color = route.route_text_color

  def loadTrips(self):
    """Loads active trips into schedule"""
    logger.info("Loading Trips")

    for route in self.schedule.GetRouteList():
      for t in db.query(Trip).filter_by(route_id=route.route_id).all():
        # trip_id = t.trip_id + '.' + service.service_id
        trip_id = t.trip_id
        trip = route.AddTrip(trip_id = trip_id, headsign=t.trip_headsign)
        trip.service_id = t.service_id
        trip.shape_id = t.shape_id
        trip.direction_id = t.direction_id
        logger.info("Loading trip_id: {0}".format(trip_id))

  def loadStops(self):
    logger.info("Loading Stops")
    used_stops_subquery = db.query(StopSeq.stop_id).distinct().subquery()
    stops_query = db.query(Stop).filter(Stop.stop_id.in_(used_stops_subquery))

    for stop in stops_query.all():
      lat = stop.stop_lat
      lng = stop.stop_lon
      stop_id = stop.stop_id
      stop = self.schedule.AddStop(lat=float(lat), lng=float(lng), 
        name=stop.stop_name, stop_id=stop_id)
      stop.stop_code = stop.stop_id

  def loadStopTimes(self):
    """Adding Stop Times from trip start times"""
    logger.info("Loading Stop Times")

    for trip in self.schedule.GetTripList():
      # trip_id, service_id = trip['trip_id'].split('.')

      for stopTime in db.query(StopTime).filter_by(trip_id=trip.trip_id).\
        order_by(StopTime.stop_sequence).all():
        stop = self.schedule.GetStop(stopTime.stop_id)
        stop_time = stopTime.arrival_time
        if stop_time:
          trip.AddStopTime(stop,stop_time=stop_time)
        else:
          trip.AddStopTime(stop)

  def loadShapes(self):
    logger.info("Loading Shapes")

    usedShapes = set([trip['shape_id'] for trip in self.schedule.GetTripList()])

    for shape_id in usedShapes:
      shape_query = db.query(Shape).filter_by(shape_id=shape_id).order_by(Shape.shape_pt_sequence)
      shape = transitfeed.Shape(shape_id=shape_id)
      for pt in shape_query.all():
        shape.AddPoint(lat=pt.shape_pt_lat, lon=pt.shape_pt_lon)
      self.schedule.AddShapeObject(shape)

  def loadFrequencies(self):
      logger.info("Loading Frequencies")

      for freq in db.query(Frequency).all():

        f = transitfeed.Frequency({'trip_id':freq.trip_id, 
            'start_time':freq.start_time, 
            'end_time':freq.end_time, 
            'headway_secs':freq.headway_secs})
        f.AddToSchedule(self.schedule)

  def loadFeedInfo(self):
    logger.info("Load Feed Info")

    keys = ['feed_publisher_name', 'feed_start_date', 'feed_version', 
        'feed_end_date', 'feed_lang', 'feed_publisher_url']
    feed_info_txt = StringIO.StringIO()
    writer = csv.DictWriter(feed_info_txt, keys)
    writer.writeheader()
    for info in db.query(FeedInfo).all():
      writer.writerow(info.as_dict)
    with zipfile.ZipFile(self.filename, "a") as z:
        z.writestr('feed_info.txt', feed_info_txt.getvalue())
