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

from flask_script import Manager
from flask_script.commands import Clean, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

celery_app = create_celery_app(app)


def make_shell_context():
    return dict(app=app, celery_app=celery_app, db=db, Route=Route, Trip=Trip,
      Shape=Shape, Stop=Stop, StopSeq=StopSeq, TripStartTime=TripStartTime,
      CalendarDate=CalendarDate, Calendar=Calendar, Agency=Agency,
      FeedInfo=FeedInfo, Feed=Feed, User=User, Role=Role, ShapePath=ShapePath)


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
