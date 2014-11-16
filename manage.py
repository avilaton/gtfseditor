#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from server import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

Session = sessionmaker(bind=engine)
db = scoped_session(Session)

from server.models import *

from server.collections.interpolation import Interpolator
from server.collections.populator import StopTimesFactory
from server.collections.stop_sequence import StopSequence
from server.services.defaults import loadDefaultTripStartTimes

import os
import glob
import zipfile
import optparse
import csv
import codecs

TMP_FOLDER = 'tmp/'

def create_all():
  logger.info("Creating all tables")
  from server.models import Base
  Base.metadata.create_all(engine)

def drop_all():
  logger.info("Droping all tables")
  from server.models import Base
  Base.metadata.drop_all(engine)

def extract(filename, dest):
  """extract for debuging"""
  if not os.path.exists(dest):
    os.makedirs(dest)
  else:
    for oldfile in glob.glob(dest + '*'):
      os.remove(oldfile)

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

def generateShapePtSequence():
  ins = Shape.__table__.insert()
  for shape in db.query(Shape.shape_id).distinct():
    
    logger.info("generate sequence for shape_id: %s", shape.shape_id)

    shapeQuery = db.query(Shape).filter_by(shape_id = shape.shape_id)
    shape_pts = shapeQuery.order_by(Shape.shape_pt_time)

    pts = []
    for i, pt in enumerate(shape_pts):
      pt.shape_pt_sequence = i
      pts.append(pt.as_dict)
      db.delete(pt)
    # db.commit()
    db.execute(ins, pts)

  db.commit()

def generateStopSeq():
  logger.info("Generating Stop Sequences")

  import time
  t0 = time.time()

  ins = StopSeq.__table__.insert()
  for trip in db.query(StopSeq.trip_id).distinct():
    
    logger.info("generate sequence for trip_id: %s", trip.trip_id)

    query = db.query(StopSeq).filter_by(trip_id = trip.trip_id)
    trip_pts = query.order_by(StopSeq.stop_time)

    pts = []
    for i, pt in enumerate(trip_pts):
      pt.stop_sequence = i
      pts.append(pt.as_dict)
      db.delete(pt)
    db.execute(ins, pts)

  db.commit()
  logger.info("Time elapsed %s",time.time()-t0)

def readCsv(session, engine, Model, filename, mode=None):
  logger.info("Importing " + Model.__tablename__ + " from : %s", filename)
  with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    if not mode:
      keyMap = {field:field for field in reader.fieldnames}
      for row in reader:
        d = {v:codecs.decode(row[k],'utf8') for k, v in keyMap.items()}
        model = Model(**d)
        session.merge(model)
      session.commit()
    elif mode in ['direct']:
      engine.execute(Model.__table__.delete())
      insertStmt = Model.__table__.insert()
      engine.execute(insertStmt, [row for row in reader])

def import_csv():
  Session = sessionmaker(bind=engine)
  session = scoped_session(Session)
  FOLDER = 'tmp/incoming/'

  readCsv(session, engine, Agency, FOLDER + 'agency.csv')
  readCsv(session, engine, FeedInfo, FOLDER + 'feed_info.csv')
  readCsv(session, engine, Calendar, FOLDER + 'calendar.csv')
  readCsv(session, engine, CalendarDate, FOLDER + 'calendar_dates.csv')
  readCsv(session, engine, Stop, FOLDER + 'stops.csv')
  readCsv(session, engine, Route, FOLDER + 'routes.csv')
  readCsv(session, engine, Shape, FOLDER + 'shapes.csv', mode='direct')
  readCsv(session, engine, Trip, FOLDER + 'trips.csv')
  readCsv(session, engine, TripStartTime, FOLDER + 'trips_start_times.csv')
  readCsv(session, engine, StopSeq, FOLDER + 'stop_times.csv', mode='direct')

if __name__ == '__main__':
  usage = """usage: %prog [options] command
where command can be one of:

  create-all        Create all tables in DB
  drop-all          Drop all tables in DB
  load-defaults     Load defaults into DB
  import-csv        Read Csv files into DB
  build             create GTFS feed
  interpolate       interpolate trip times
  pop-times         generates stop times from stop sequences
  sort-trip         sort trip stops along shape
  gen-stop-seq      Generate stop_sequence values from stop_time
  gen-shape-pt-seq  Generate shape point sequence from shape_pt_time
  """


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
  else:
    command = args[0]

  if command == 'build':
    feed = Feed()
    feedFile = feed.build()

    with open(TMP_FOLDER + feed.filename, 'wb') as f:
      f.write(feedFile.getvalue())

    if opts.validate:
      feed.validate()

    if opts.extract:
      extract(TMP_FOLDER + feed.filename, 'tmp/extracted/')

  elif command == 'create-all':
    create_all()
  elif command == 'drop-all':
    drop_all()
  elif command == 'load-defaults':
    loadDefaultTripStartTimes(db)
  elif command == 'import-csv':
    import_csv()
  elif command == 'interpolate':
    generate_interpolated_stop_times()
  elif command == 'pop-times':
    generate_stop_times_from_stop_seqs()
  elif command == 'sort-trip':
    sort_trips()
  elif command == 'update-dist':
    update_distance_traveled()
  elif command == 'gen-stop-seq':
    generateStopSeq()
  elif command == 'gen-shape-pt-seq':
    generateShapePtSequence()
  elif command == 'mza':
    drop_all()
    create_all()
    import_csv()
  elif command == 'mza-gen':
    generateStopSeq()
    generateShapePtSequence()
    # generate_stop_times_from_stop_seqs()
  else:
    parser.error("command not found")

