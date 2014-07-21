#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import transitfeed

from server import engine
from server.models import Route
from server.models import Agency
from server.models import Trip
from server.models import Calendar
from server.models import CalendarDate
from server.models import Stop
from server.models import StopSeq

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

Session = sessionmaker(bind=engine)
db = scoped_session(Session)

class Feed(object):
  """GTFS schedule feed factory"""
  def __init__(self, arg):
    self.arg = arg
    self.schedule = transitfeed.Schedule()

  def __repr__(self):
    return 'a feed' 

  def build(self):
    logger.info("Feed build started")
    self.loadAgencies()
    self.loadCalendar()
    self.loadCalendarDates()
    self.loadRoutes()
    self.loadTrips()
    self.loadStops()

    self.schedule.WriteGoogleTransitFeed('tmp/test.zip')

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
    for s in db.query(Calendar).all():
      service = transitfeed.ServicePeriod()
      service.SetServiceId(s.service_id)
      service.SetStartDate(str(s.start_date))
      service.SetEndDate(str(s.end_date))
      service.SetDayOfWeekHasService(0, bool(s.monday) )
      service.SetDayOfWeekHasService(1, bool(s.tuesday) )
      service.SetDayOfWeekHasService(2, bool(s.wednesday) )
      service.SetDayOfWeekHasService(3, bool(s.thursday) )
      service.SetDayOfWeekHasService(4, bool(s.friday) )
      service.SetDayOfWeekHasService(5, bool(s.saturday) )
      service.SetDayOfWeekHasService(6, bool(s.sunday) )
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
      route_id = route['route_id']
      for t in db.query(Trip).filter_by(route_id=route_id).all():
        for service in self.schedule.GetServicePeriodList():
          trip_id = t.trip_id + '.' + service.service_id
          trip = route.AddTrip(trip_id = trip_id, headsign=t.trip_headsign)
          trip.service_id = service.service_id
          trip.shape_id = t.trip_id
          trip.direction_id = t.direction_id
          logger.info("Loading trip_id: {0}".format(trip_id))

  def loadStops(self):
    logger.info("Loading Stops")
    used_stops_subquery = db.query(StopSeq.stop_id).distinct().subquery()
    query = db.query(Stop).filter(Stop.stop_id.in_(used_stops_subquery))

    for stop in query.all():
      lat = stop.stop_lat
      lng = stop.stop_lon
      stop_id = stop.stop_id
      stop = self.schedule.AddStop(lat=float(lat), lng=float(lng), 
        name=stop.stop_name, stop_id=stop_id)
      stop.stop_code = stop.stop_id
