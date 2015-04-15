#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from transitfeed import TimeToSecondsSinceMidnight
from transitfeed import FormatSecondsSinceMidnight

from ..models import *


class StopTimesFactory(object):
  """docstring for StopTimesFactory"""

  def __init__(self, db):
    self.db = db

  def frequency_mode(self, trip_id=None, commit=False):
    """ In Frequency mode, copy each stop sequence to the stop times table"""
    trip_stop_sequence = self.db.query(StopSeq).filter_by(trip_id=trip_id).all()

    for stopSeq in trip_stop_sequence:
      stop_seq_dict = stopSeq.to_json
      stop_seq_dict.update({
        'arrival_time': stopSeq.stop_time,
        'departure_time': stopSeq.stop_time
        })
      stop_seq_dict.pop('stop_time')
      stopTime = StopTime(**stop_seq_dict)
      self.db.merge(stopTime)
    if commit:
      self.db.commit()

  @staticmethod
  def offsetStartTimes(trip_id, trip_stop_sequence, startTimeRow):
    start_time_secs = TimeToSecondsSinceMidnight(startTimeRow.start_time)
    new_trip_id = '.'.join([str(trip_id), str(startTimeRow.service_id), 
      startTimeRow.start_time])
    for stopSeq in trip_stop_sequence:
      stop_seq_dict = stopSeq.to_json

      stop_time_elapsed = stopSeq.stop_time
      if stop_time_elapsed:
        stop_time_secs = TimeToSecondsSinceMidnight(stop_time_elapsed)
        stop_time_total_secs = stop_time_secs + start_time_secs
        stop_time = FormatSecondsSinceMidnight(stop_time_total_secs)
      else:
        stop_time = stop_time_elapsed

      stop_seq_dict.update({
        'arrival_time': stop_time,
        'departure_time': stop_time,
        'trip_id': new_trip_id
        })
      stop_seq_dict.pop('stop_time')
      yield stop_seq_dict    

  def initial_times_mode(self, trip_id=None, commit=False):
    """ In Frequency mode, copy each stop sequence to the stop times table"""
    logger.info("Populating stop times for trip_id:" + trip_id)
    trip_stop_sequence = self.db.query(StopSeq).filter_by(trip_id=trip_id).\
      order_by(StopSeq.stop_sequence).all()
    trip_start_times = self.db.query(TripStartTime).filter_by(trip_id=trip_id).all()
    if not trip_start_times:
      trip_start_times = self.db.query(TripStartTime).filter_by(trip_id='default').all()

    for startTimeRow in trip_start_times:
      for stop_time in self.offsetStartTimes(trip_id, trip_stop_sequence, startTimeRow):
        stopTime = StopTime(**stop_time)
        self.db.merge(stopTime)

    if commit:
      self.db.commit()

  def allSeqs(self):
    logger.info("Populating initial times for all trips")
    for trip in self.db.query(StopSeq.trip_id).distinct().all():
      # self.frequency_mode(trip_id=trip.trip_id)
      self.initial_times_mode(trip_id=trip.trip_id)
    self.db.commit()

  def allActiveRoutes(self):
    logger.info("Populating initial times for all active routes")

    for route in self.db.query(Route).filter(Route.active != None).all():
      logger.info("Populating times for route_id: {0}".format(route.route_id))
      for trip in self.db.query(Trip).filter_by(route_id=route.route_id).all():
        self.initial_times_mode(trip_id=trip.trip_id)
    self.db.commit()
