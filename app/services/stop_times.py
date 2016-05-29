#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from transitfeed import TimeToSecondsSinceMidnight
from transitfeed import FormatSecondsSinceMidnight


def offset_sequence_times(trip_stop_sequence, start_time):
  try:
    start_time_secs = TimeToSecondsSinceMidnight(start_time)
  except Exception, e:
    print e
    return

  for stopSeq in trip_stop_sequence:
    stop_time_elapsed = stopSeq.stop_time
    if stop_time_elapsed:
      stop_time_secs = TimeToSecondsSinceMidnight(stop_time_elapsed)
      stop_time_total_secs = stop_time_secs + start_time_secs
      stop_time = FormatSecondsSinceMidnight(stop_time_total_secs)
    else:
      stop_time = stop_time_elapsed

    yield {'arrival_time': stop_time, 'stop_id': stopSeq.stop_id}
