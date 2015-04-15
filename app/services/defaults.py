#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from datetime import date, datetime, time, timedelta

from ..models import TripStartTime

def startTimes():
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
    i += 1
    yield TripStartTime(**model)
