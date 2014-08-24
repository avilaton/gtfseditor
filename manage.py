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

from server.models import StopSeq
from server.models import Shape

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

def drop_all():
  from server.models import Base
  Base.metadata.drop_all(engine)
  # db.query(Stop).delete()
  # db.query(Shape).delete()
  # db.query(StopSeq).delete()
  # db.query(Route).delete()
  # db.query(Trip).delete()
  # db.commit()  

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

if __name__ == '__main__':
  usage = """usage: %prog [options] command
where command can be one of:

  create-all        Initialize Database engine issuing CREATE statements for
                    each table
  build             create GTFS feed
  interpolate       interpolate trip times
  pop-times         generates stop times from stop sequences
  sort-trip         sort trip stops along shape
  gen-stop-seq      Generate stop_sequence values from stop_time
  gen-shape-pt-seq  Generate shape point sequence from shape_pt_time"""


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
    init_db()
  elif command == 'drop-all':
    drop_all()
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
    generateStopSeq()
    generateShapePtSequence()
    generate_stop_times_from_stop_seqs()
  else:
    parser.error("command not found")

