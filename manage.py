#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
from app import create_app, db
from app.models import Route
from app.models import Trip
from app.services.feed import Feed

from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


TMP_FOLDER = '.tmp/'

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
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
    return dict(app=app, db=db, Route=Route, Trip=Trip)

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
    extractZip(TMP_FOLDER + feed.filename, 'tmp/extracted/')

if __name__ == '__main__':
    manager.run()
