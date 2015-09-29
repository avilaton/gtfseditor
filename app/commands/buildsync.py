
import zipfile
import glob

from app.services.feed import Feed
from app.services.s3 import S3



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

