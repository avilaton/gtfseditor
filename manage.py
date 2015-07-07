#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import codecs
import glob
import zipfile
from config import config
from app import create_app
from app import db
from app.models import *
from app.services.feed import Feed
from app.services.s3 import S3
from app.services.sequence import StopSequence as Sequence

from flask.ext.script import Manager
from flask.ext.script import Shell
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand

TMP_FOLDER = config[os.getenv('FLASK_CONFIG') or 'default'].TMP_FOLDER
BUILD_MODE = config[os.getenv('FLASK_CONFIG') or 'default'].BUILD_MODE

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


from app.tasks import celery_app

manager = Manager(app)
migrate = Migrate(app, db)


def readCsv(Model, filename, mode=None):
  print("Importing " + Model.__tablename__ + " from : " + filename)
  with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    if not mode:
      for row in reader:
        d = {field: (codecs.decode(row[field],'utf8') if row[field] else None)
          for field in reader.fieldnames}
        model = Model(**d)
        db.session.merge(model)
      db.session.commit()
    elif mode in ['direct']:
      db.engine.execute(Model.__table__.delete())
      insertStmt = Model.__table__.insert()
      db.engine.execute(insertStmt, [row for row in reader])

class DictUnicodeProxy(object):
  def __init__(self, d):
    self.d = d
  def __iter__(self):
    return self.d.__iter__()
  def get(self, item, default=None):
    i = self.d.get(item, default)
    if isinstance(i, unicode):
      return i.encode('utf-8')
    return i

def exportToCsv(Model, filename, mode=None):
  print("Exporting " + Model.__tablename__ + " to : " + filename)
  with open(filename + Model.__tablename__ + ".csv", 'w') as csvfile:
    fieldnames = Model.__table__.columns.keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in Model.query.all():
      writer.writerow(DictUnicodeProxy(row.to_json))



def extractZip(filename, dest):
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


def make_shell_context():
    return dict(app=app, db=db, Route=Route, Trip=Trip, Sequence=Sequence,
      Shape=Shape, Stop=Stop, StopSeq=StopSeq, TripStartTime=TripStartTime,
      CalendarDate=CalendarDate, Calendar=Calendar, Agency=Agency,
      FeedInfo=FeedInfo, Feed=Feed, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade

    # migrate database to latest revision
    upgrade()

@manager.command
def buildfeed(validate=False, extract=False, upload=False):
  """Build feed task"""
  from app.tasks import buildFeed

  buildFeed.run(validate=validate, extract=extract, upload=upload)

@manager.command
def build(validate=False, extract=False, upload=False):
  """Build feed to .tmp folder"""

  if not os.path.isdir(TMP_FOLDER):
    os.makedirs(TMP_FOLDER)

  feed = Feed(db=db.session)
  feedFile = feed.build(mode=BUILD_MODE)

  with open(TMP_FOLDER + feed.filename, 'wb') as f:
    f.write(feedFile.getvalue())

  if validate:
    feed.validate()

  if extract:
    extractZip(TMP_FOLDER + feed.filename, TMP_FOLDER + 'extracted/')

  if upload:
    BUCKET_NAME = 'gtfseditor-feeds'
    s3service = S3(BUCKET_NAME)
    s3service.config(app.config)
    s3service.uploadFileObj(feed.filename, feedFile)

@manager.command
def updatedistances():
  """Update traveled distances for every trip"""

  trips = Trip.query.all()
  total = len(trips)

  for i, trip in enumerate(trips):
    print("{2}/{1} updating distances for trip_id={0}".format(trip.trip_id, total, i))
    seq = Sequence(trip_id=trip.trip_id)
    seq.updateDistances()

@manager.command
def sorttrips():
  """Update traveled distances for every trip"""

  trips = Trip.query.all()
  total = len(trips)

  for i, trip in enumerate(trips):
    print("{2}/{1} sorting stops for for trip_id={0}".format(trip.trip_id, total, i))
    seq = Sequence(trip.trip_id)
    seq.sortStops()

@manager.command
def interpolatetimes():
  """Interpolate trip times for every trip"""

  trips = Trip.query.all()
  total = len(trips)

  for i, trip in enumerate(trips):
    print("{2}/{1} interpolating times for trip_id={0}".format(trip.trip_id, total, i))
    seq = Sequence(trip.trip_id)
    seq.interpolateTimes()
  db.session.commit()

@manager.command
def renamestops():
  """Creates stop names from other columns"""

  stops = Stop.query.all()
  total = len(stops)

  for i, stop in enumerate(stops):
    stop.stop_calle = stop.stop_calle.title()
    stop_name = ' '.join([stop.stop_calle, stop.stop_numero]).strip()
    if not stop_name:
      stop_name = stop.stop_id
    stop.stop_name = stop_name
    db.session.merge(stop)
    print("{2}/{1} Stop_id: {0} renamed to: {3}".format(stop.stop_id, total, i, stop_name.encode('utf8')))
  db.session.commit()

@manager.command
def importCardCodes(filename):
  """Creates stop names from other columns"""
  import csv

  with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      codigo = row["codigo"].strip()
      trip_id = row["trip_id"].strip()
      card_code = codigo[-3:]
      route_id = codigo[:-3]
      if route_id.isdigit():
        route_id = route_id.zfill(3)
      trip = Trip.query.filter_by(trip_id=trip_id).first()
      print codigo, card_code, trip_id, trip
      if trip:
        trip.card_code = card_code
        db.session.merge(trip)
  db.session.commit()

@manager.command
def importInitTimes(filename, grupo):
  """Creates stop names from other columns
    grupo is one of 01, 02, 03, ...
  """
  import csv

  codes = {}
  with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      print row
      card_code = row["codigo"]
      row["service_id"] = row["service_id"].lower()
      row["trip_start_time"] = row["trip_start_time"] + ":00"
      codes.setdefault(card_code, [])
      codes[card_code].append(row)

  startTimeRows = []

  for card_code, times in codes.items():
    print "\n", card_code
    trips = Trip.query.order_by(Trip.route_id).\
      filter(Trip.route_id.ilike(grupo + '%'), Trip.card_code == card_code).all()
    for trip in trips:
      for time in times:
        tripStartTime = TripStartTime(service_id=time["service_id"],
          start_time=time["trip_start_time"])
        tripStartTime.trip_id = trip.trip_id
        startTimeRows.append(tripStartTime)
        print tripStartTime.to_json

  db.session.add_all(startTimeRows)
  db.session.flush()

@manager.command
def backup(dbname):
  import subprocess
  import datetime

  now = datetime.datetime.now()
  # timestamp = now.strftime("%Y-%m-%d")
  timestamp = now.isoformat()
  filename = dbname + "_" + timestamp + ".tar"
  folderId = "0Bx2pbTBESHr7ZWdhV09EOUlPVjA"
  print("backing up as " + filename)
  subprocess.call("pg_dump -Ft " + dbname + " > " + filename, shell=True)
  print("uploading to drive folder " + folderId)
  subprocess.call("drive upload -f " + filename + " -p " + folderId, shell=True)


@manager.command
def activateRoute(route_id=False):

  routes = Route.query.all()

  for route in routes:
    if not route_id:
      route.active = True
    else:
      if route.route_id in [route_id]:
        route.active = True
      else:
        route.active = False
    db.session.merge(route)
  db.session.commit()


@manager.command
def importCsv(modelname, filename, mode=None):
  Model = globals()[modelname]
  readCsv(Model, filename, mode=mode)


@manager.command
def importCba(folder):
  """Usage:
  FLASK_CONFIG=local ./manage.py importCba <FOLDER>
  """

  importCsv("Agency", folder + "agency.csv")
  importCsv("Calendar", folder + 'calendar.csv')
  importCsv("CalendarDate", folder + 'calendar_dates.csv')
  importCsv("FareAttribute", folder + 'fare_attributes.csv')
  importCsv("FareRule", folder + 'fare_rules.csv')
  importCsv("FeedInfo", folder + 'feed_info.csv')
  importCsv("Route", folder + 'routes.csv')
  importCsv("RouteFrequency", folder + 'route_frequencies.csv')
  importCsv("Stop", folder + 'stops.csv')
  importCsv("Shape", folder + 'shapes.csv', mode='direct')
  importCsv("Trip", folder + 'trips.csv')
  importCsv("TripStartTime", folder + 'trips_start_times.csv')
  importCsv("StopSeq", folder + 'stop_seq.csv', mode='direct')
  importCsv("StopTime", folder + 'stop_times.csv')
  importCsv("Frequency", folder + 'frequencies.csv')


@manager.command
def export(folder=".tmp/export/"):

  exportToCsv(Agency, folder)
  exportToCsv(Calendar, folder)
  exportToCsv(CalendarDate, folder)
  exportToCsv(FareAttribute, folder)
  exportToCsv(FareRule, folder)
  exportToCsv(FeedInfo, folder)
  exportToCsv(RouteFrequency, folder)
  exportToCsv(Route, folder)
  exportToCsv(Stop, folder)
  exportToCsv(Shape, folder)
  exportToCsv(Trip, folder)
  exportToCsv(TripStartTime, folder)
  exportToCsv(StopSeq, folder)
  exportToCsv(StopTime, folder)
  exportToCsv(Frequency, folder)


if __name__ == '__main__':
    manager.run()
