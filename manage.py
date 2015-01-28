#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
from app import create_app
from app import db
from app.models import *
from app.services.feed import Feed
from app.services.sequence import StopSequence as Sequence

from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


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
      FeedInfo=FeedInfo)

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

if __name__ == '__main__':
    manager.run()
