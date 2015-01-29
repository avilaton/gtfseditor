from . import db
from . import create_celery_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

celery_app = create_celery_app()

@celery_app.task(bind=True)
def sendEmail(self, msg):
    from time import sleep
    logger.info("task started")
    sleep(2)
    print self.request.id
    return msg

@celery_app.task
def buildFeed(validate=False):
  """Build feed to .tmp folder"""
  import os
  from app.services.feed import Feed

  TMP_FOLDER = '.tmp/'

  if not os.path.isdir(TMP_FOLDER):
    os.makedirs(TMP_FOLDER)
  logger.info("Temp folder created")

  feed = Feed(db=db.session)
  feedFile = feed.build()

  with open(TMP_FOLDER + feed.filename, 'wb') as f:
    f.write(feedFile.getvalue())

  if validate:
    feed.validate()
