#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import transitfeed

from server import engine
from server.models import StopSeq

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

Session = sessionmaker(bind=engine)
db = scoped_session(Session)

class Interpolator(object):
  """docstring for Interpolator"""
  def __init__(self):
    self.db = db

  def bySpeed(self, trip_id=None, speed=19, commit=False):
    trip_stops = db.query(StopSeq).filter_by(trip_id=trip_id).all()

    for i, stopSeq in enumerate(trip_stops):
      dist_traveled = float(stopSeq.shape_dist_traveled)
      stop_time_secs = int(3600*dist_traveled/(speed))
      stop_time = transitfeed.FormatSecondsSinceMidnight(stop_time_secs)
      stopSeq.stop_time = stop_time
      db.merge(stopSeq)
    if commit:
      db.commit()

  def allSeqs(self):
    for trip in db.query(StopSeq.trip_id).distinct().all():
      logger.info("Interpolating trip_id:" + trip.trip_id)
      self.bySpeed(trip_id=trip.trip_id)
    db.commit()
