#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
from config import config
from app import create_app
from app import db
from app.models import *
from app.services.feed import Feed
from app.services.sequence import StopSequence as Sequence

from flask.ext.script import Manager
from flask.ext.script import Shell
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand

TMP_FOLDER = config[os.getenv('FLASK_CONFIG') or 'default'].TMP_FOLDER

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

from app.tasks import celery_app

manager = Manager(app)
migrate = Migrate(app, db)


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
      FeedInfo=FeedInfo, Feed=Feed)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade

    # migrate database to latest revision
    upgrade()

@manager.command
def build(validate=False, extract=False):
  """Build feed to .tmp folder"""

  if not os.path.isdir(TMP_FOLDER):
    os.makedirs(TMP_FOLDER)

  feed = Feed(db=db.session)
  feedFile = feed.build()

  with open(TMP_FOLDER + feed.filename, 'wb') as f:
    f.write(feedFile.getvalue())

  if validate:
    feed.validate()

  if extract:
    extractZip(TMP_FOLDER + feed.filename, TMP_FOLDER + 'extracted/')

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
  """Creates stop names from other columns"""
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
def backup():
  import subprocess
  import datetime

  now = datetime.datetime.now()
  # timestamp = now.strftime("%Y-%m-%d")
  timestamp = now.isoformat()
  filename = "mza_" + timestamp + ".tar"
  folderId = "0Bx2pbTBESHr7ZWdhV09EOUlPVjA"
  print("backing up as " + filename)
  subprocess.call("pg_dump -Ft mza > " + filename, shell=True)
  print("uploading to drive folder " + folderId)
  subprocess.call("drive upload -f " + filename + " -p " + folderId, shell=True)


if __name__ == '__main__':
    manager.run()
