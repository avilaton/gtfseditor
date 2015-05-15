import os
import glob
import zipfile

from . import db
from . import create_celery_app
from celery.utils.log import get_task_logger
from .services.s3 import S3

logger = get_task_logger(__name__)

celery_app = create_celery_app()


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


@celery_app.task(bind=True)
def sendEmail(self, msg):
    logger.info("send email task started")
    from time import sleep
    sleep(2)
    logger.info("Task id is {0}".format(self.request.id))
    return msg

@celery_app.task
def buildFeed(validate=False, extract=False, upload=False):
  """Build feed to .tmp folder"""
  logger.info("build feed task started")

  from app.services.feed import Feed

  TMP_FOLDER = celery_app.conf.TMP_FOLDER

  if not os.path.isdir(TMP_FOLDER):
    os.makedirs(TMP_FOLDER)

  feed = Feed(db=db.session)
  feedFile = feed.build()
  feed.saveTo(TMP_FOLDER)

  if extract:
    extractZip(TMP_FOLDER + feed.filename, TMP_FOLDER + 'extracted/')

  if validate:
    feed.validate()

  if upload:
    s3service = S3(celery_app.conf.AWS_S3_BUCKET_NAME)
    s3service.config(celery_app.conf)
    logger.info('Uploading {0} to Amazon S3 bucket {1}'.format(feed.filename,
      celery_app.conf.AWS_S3_BUCKET_NAME))
    s3service.uploadFileObj(feed.filename, feedFile)

  return 'success'

@celery_app.task
def listDir():
  """Build feed to .tmp folder"""
  logger.info("listing files in TMP folder")
  import os

  if not os.path.isdir(celery_app.conf.TMP_FOLDER):
    os.makedirs(celery_app.conf.TMP_FOLDER)

  files = os.listdir(celery_app.conf.TMP_FOLDER)

  return files