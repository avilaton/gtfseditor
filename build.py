#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
import optparse

from server.models import Feed

TMP_FOLDER = 'tmp/'

def extract(filename, dest):
    """extract for debuging"""
    if not os.path.exists(dest):
      os.makedirs(dest)

    with zipfile.ZipFile(filename, "r") as z:
      for filename in z.namelist():
        with file(dest + filename, "w") as outfile:
          outfile.write(z.read(filename))

if __name__ == '__main__':
  parser = optparse.OptionParser()
  parser.add_option('-v', '--validate', help='Execute validation at the end', 
      action='store_true', dest='validate')
  parser.add_option('-e', '--extract', help='Extract compiled feed', 
      action='store_true', dest='extract')
  (opts, args) = parser.parse_args()

  feed = Feed()
  feedFile = feed.build()

  with open(TMP_FOLDER + feed.filename, 'wb') as f:
    f.write(feedFile.getvalue())

  if opts.validate:
    feed.validate()

  if opts.extract:
    extract(TMP_FOLDER + feed.filename, 'tmp/extracted/')
