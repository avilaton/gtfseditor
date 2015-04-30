from . import db
from . import create_celery_app
from celery.utils.log import get_task_logger
from .services.s3 import S3

logger = get_task_logger(__name__)

celery_app = create_celery_app()

@celery_app.task(bind=True)
def sendEmail(self, msg):
    logger.info("send email task started")
    from time import sleep
    sleep(2)
    logger.info("Task id is {0}".format(self.request.id))
    return msg

@celery_app.task
def buildFeed(validate=False):
  """Build feed to .tmp folder"""
  logger.info("build feed task started")
  import os
  from app.services.feed import Feed

  if not os.path.isdir(celery_app.conf.TMP_FOLDER):
    os.makedirs(celery_app.conf.TMP_FOLDER)

  feed = Feed(db=db.session)
  feedFile = feed.build()
  feed.saveTo(celery_app.conf.TMP_FOLDER)

  with open(celery_app.conf.TMP_FOLDER + feed.filename, 'wb') as f:
    f.write(feedFile.getvalue())

  if validate:
    feed.validate()

  s3service = S3(celery_app.conf.AWS_S3_BUCKET_NAME)
  s3service.config(celery_app.conf)

  logger.info('Uploading %s to Amazon S3 bucket %s'.format(feed.filename,
    celery_app.conf.AWS_S3_BUCKET_NAME))

  s3service.uploadFileObj(feed.filename, feedFile)

@celery_app.task
def listDir():
  """Build feed to .tmp folder"""
  logger.info("listing files in TMP folder")
  import os

  if not os.path.isdir(celery_app.conf.TMP_FOLDER):
    os.makedirs(celery_app.conf.TMP_FOLDER)

  files = os.listdir(celery_app.conf.TMP_FOLDER)

  return files