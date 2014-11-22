#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from server.models import TripStartTime

from datetime import date, datetime, time, timedelta

def loadDefaultTripStartTimes(db):
  logger.info('Loading default Trip Start Times to DB')
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
    tripStartTime = TripStartTime(**model)
    db.merge(tripStartTime)
    i += 1
  db.commit()
