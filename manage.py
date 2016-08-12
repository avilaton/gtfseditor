#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from config import config
from app import create_app
from app import create_celery_app
from app import db
from app.models import *
from app.services.feed import Feed

from app.commands import BuildFeed
from app.commands import MigrateShapes
from app.commands import ExportCSV
from app.commands import DumpData
from app.commands import LoadData
from app.commands import Deploy

from flask.ext.script import Manager
from flask_script.commands import Clean, Shell
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

celery_app = create_celery_app(app)


def make_shell_context():
    return dict(app=app, celery_app=celery_app, db=db, Route=Route, Trip=Trip,
      Shape=Shape, Stop=Stop, StopSeq=StopSeq, TripStartTime=TripStartTime,
      CalendarDate=CalendarDate, Calendar=Calendar, Agency=Agency,
      FeedInfo=FeedInfo, Feed=Feed, User=User, Role=Role, ShapePath=ShapePath)

<<<<<<< HEAD
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade

    # migrate database to latest revision
    upgrade()
    # create user roles
    Role.insert_roles()

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
=======
>>>>>>> develop

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('buildfeed', BuildFeed)
manager.add_command('export', ExportCSV)
manager.add_command('dumpdata', DumpData)
manager.add_command('loaddata', LoadData)
manager.add_command('deploy', Deploy)
manager.add_command('migrate_shapes', MigrateShapes)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('clean', Clean)


if __name__ == '__main__':
    manager.run()
