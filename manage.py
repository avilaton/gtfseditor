#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server import engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

Session = sessionmaker(bind=engine)
db = scoped_session(Session)

from server.collections.interpolation import Interpolator
from server.collections.populator import StopTimesFactory
from server.collections.stop_sequence import StopSequence

import os
import zipfile
import optparse

from server.models import Feed

TMP_FOLDER = 'tmp/'

def init_db():
  from server.models import Base
  Base.metadata.create_all(engine)


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
  interpolator.allSeqs()

def generate_stop_times_from_stop_seqs():
  stopTimesFactory = StopTimesFactory()
  # stopTimesFactory.frequency_mode(trip_id='10.ida', commit=True)
  # stopTimesFactory.initial_times_mode(trip_id='a_trip_id', commit=True)
  stopTimesFactory.allSeqs()

def sort_trips():
  trip = StopSequence('a_trip_id')
  trip.sortStops()

def update_distance_traveled():
  trip = StopSequence('a_trip_id')
  trip.updateDistances()

if __name__ == '__main__':
  usage = """usage: %prog [options] command
where command can be one of:

  init-db         Initialize Database engine issuing all CREATE statements
  build           create GTFS feed
  interpolate     interpolate trip times
  pop-times       generates stop times from stop sequences
  sort-trip       sort trip stops along shape"""


  parser = optparse.OptionParser(usage=usage)
  parser.add_option('-v', '--validate', help='Execute validation at the end', 
      action='store_true', dest='validate')
  parser.add_option('-e', '--extract', help='Extract compiled feed', 
      action='store_true', dest='extract')
  parser.add_option('-d', '--dry-run', help='Do not save changes to db', 
      action='store_true', dest='dry-run')
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

  elif args[0] == 'init-db':
    init_db()
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

