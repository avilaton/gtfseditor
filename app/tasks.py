from . import db
from . import create_celery_app

celery_app = create_celery_app()

@celery_app.task
def sendEmail(msg):
    from time import sleep
    sleep(10)
    return msg

@celery_app.task
def buildFeed(validate=False):
  """Build feed to .tmp folder"""
  import os
  from app.services.feed import Feed

  TMP_FOLDER = '.tmp/'

  if not os.path.isdir(TMP_FOLDER):
    os.makedirs(TMP_FOLDER)

  feed = Feed(db=db.session)
  feedFile = feed.build()

  with open(TMP_FOLDER + feed.filename, 'wb') as f:
    f.write(feedFile.getvalue())

  if validate:
    feed.validate()
