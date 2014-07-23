#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
import optparse

from server.models import Feed

def extract(filename, destination):
    """extract for debuging"""
    with zipfile.ZipFile(filename, "r") as z:
        if not os.path.exists(destination):
            os.makedirs(destination)
        for filename in z.namelist():
            with file(destination + filename, "w") as outfile:
                outfile.write(z.read(filename))

if __name__ == '__main__':
  parser = optparse.OptionParser()
  parser.add_option('-v', '--validate', help='Execute validation at the end', 
      action='store_true', dest='validate')
  parser.add_option('-e', '--extract', help='Extract compiled feed', 
      action='store_true', dest='extract')
  (opts, args) = parser.parse_args()

  feed = Feed('tmp/dev.zip')
  feed.build()

  if opts.validate:
    feed.validate()

  if opts.extract:
    extract('tmp/dev.zip', 'tmp/extracted/')
