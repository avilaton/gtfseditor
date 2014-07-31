#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import transitfeed

from server import config
from server import engine
from server.models import Trip
from server.models import StopSeq
from server.models import StopTime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

Session = sessionmaker(bind=engine)
db = scoped_session(Session)

class Populator(object):
  """docstring for Populator"""
  def __init__(self):
    self.db = db

  def stop_seq_to_stop_times(self, trip_id=None, commit=False):
    seq_stops = db.query(StopSeq).filter_by(trip_id=trip_id).all()

    for stopSeq in seq_stops:
      stop_seq_dict = stopSeq.as_dict
      stop_seq_dict.update({
        'arrival_time': stopSeq.stop_time,
        'departure_time': stopSeq.stop_time
        })
      stop_seq_dict.pop('stop_time')
      stopTime = StopTime(**stop_seq_dict)
      db.merge(stopTime)
    if commit:
      db.commit()

  def allSeqs(self):
    for trip in db.query(StopSeq.trip_id).distinct().all():
      logger.info("Populating stop times for trip_id:" + trip.trip_id)
      self.stop_seq_to_stop_times(trip_id=trip.trip_id)
    db.commit()


