
import os
from app.services.feed import Feed
from . import create_app
from . import create_celery_app
from . import db

celery = create_celery_app()

TMP_FOLDER = '.tmp/'

@celery.task
def add(x, y):
    from time import sleep
    sleep(60)
    return x + y

@celery.task
def buildFeed(validate=False):
  """Build feed to .tmp folder"""

  if not os.path.isdir(TMP_FOLDER):
    os.makedirs(TMP_FOLDER)

  feed = Feed(db=db.session)
  feedFile = feed.build()

  with open(TMP_FOLDER + feed.filename, 'wb') as f:
    f.write(feedFile.getvalue())

  if validate:
    feed.validate()
