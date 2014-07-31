#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server import engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

Session = sessionmaker(bind=engine)
db = scoped_session(Session)

from server.services.interpolation import Interpolator
from server.services.populator import Populator
from server.services.trip_actions import StopSequence

import os
import zipfile
import optparse

from server.models import Feed

TMP_FOLDER = 'tmp/'

def extract(filename, dest):
  """extract for debuging"""
  if not os.path.exists(dest):
    os.makedirs(dest)

  with zipfile.ZipFile(filename, "r") as z:
    for filename in z.namelist():
      with file(dest + filename, "w") as outfile:
        outfile.write(z.read(filename))


def generate_interpolated_stop_times():
  interpolator = Interpolator()
  # interpolator.bySpeed(trip_id='10.ida')
  interpolator.allSeqs()

def generate_stop_times_from_stop_seqs():
  populator = Populator()
  # populator.stop_seq_to_stop_times(trip_id='10.ida', commit=True)
  populator.allSeqs()

def sort_trips():
  trip = StopSequence('a_trip_id')
  trip.sortStops()

def update_distance_traveled():
  trip = StopSequence('a_trip_id')
  trip.updateStopSeqDistTraveled()

if __name__ == '__main__':
  usage = """usage: %prog [options] command
where command can be one of:
  build         create GTFS feed
  interpolate   interpolate trip times
  pop-times     generates stop times from stop sequences
  sort-trip     sort trip stops along shape"""


  parser = optparse.OptionParser(usage=usage)
  parser.add_option('-v', '--validate', help='Execute validation at the end', 
      action='store_true', dest='validate')
  parser.add_option('-e', '--extract', help='Extract compiled feed', 
      action='store_true', dest='extract')
  (opts, args) = parser.parse_args()
  
  if len(args) != 1:
    parser.error("incorrect number of arguments")
  elif args[0] == 'build':
    feed = Feed()
    feedFile = feed.build()

    with open(TMP_FOLDER + feed.filename, 'wb') as f:
      f.write(feedFile.getvalue())

    if opts.validate:
      feed.validate()

    if opts.extract:
      extract(TMP_FOLDER + feed.filename, 'tmp/extracted/')

  elif args[0] == 'interpolate':
    generate_interpolated_stop_times()
  elif args[0] == 'pop-times':
    generate_stop_times_from_stop_seqs()
  elif args[0] == 'sort-trip':
    sort_trips()
  elif args[0] == 'update-dist':
    update_distance_traveled()
  else:
    parser.error("command not found")

