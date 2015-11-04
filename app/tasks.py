import os
import glob
import zipfile

from . import db
from celery.utils.log import get_task_logger
from app.services.s3 import S3
from app.services.feed import Feed

logger = get_task_logger(__name__)


def extract_zip(filename, dest):

    logger.info("Extracting %s to %s", filename, dest)

    if not os.path.exists(dest):
        os.makedirs(dest)
    else:
        for oldfile in glob.glob(dest + '*'):
            os.remove(oldfile)

    with zipfile.ZipFile(filename, "r") as z:
        for filename in z.namelist():
            print filename
            with file(dest + filename, "w") as outfile:
                outfile.write(z.read(filename))


def build_feed(celery_app, validate=False, extract=False, upload=False):
    logger.info("build feed task started")

    TMP_FOLDER = celery_app.conf.TMP_FOLDER

    if not os.path.isdir(TMP_FOLDER):
        os.makedirs(TMP_FOLDER)

    feed = Feed(db=db.session)
    feedFile = feed.build()
    feed.saveTo(TMP_FOLDER)

    if extract:
        extract_zip(TMP_FOLDER + feed.filename, TMP_FOLDER + 'extracted/')

    if validate:
        feed.validate()

    if upload:
        s3service = S3(celery_app.conf.AWS_S3_BUCKET_NAME)
        s3service.config(celery_app.conf)
        s3service.uploadFileObj(feed.filename, feedFile)


def register_tasks(celery_app):

    @celery_app.task(bind=True)
    def sendEmail(self, msg):
        logger.info("send email task started")
        from time import sleep
        sleep(2)
        logger.info("Task id is {0}".format(self.request.id))
        return msg

    @celery_app.task
    def build_feed_task(**kwargs):
        """Build feed to .tmp folder"""

        build_feed(celery_app, **kwargs)

        return 'success'
