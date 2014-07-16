#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile

from server.models import Feed

def extract(filename):
    """extract for debuging"""
    with zipfile.ZipFile(filename, "r") as z:
        if not os.path.exists('tmp/extracted/'):
            os.makedirs('tmp/extracted/')
        for filename in z.namelist():
            with file('tmp/extracted/'+filename, "w") as outfile:
                outfile.write(z.read(filename))

if __name__ == '__main__':
  feed = Feed('test')
  feed.build()
  extract('tmp/test.zip')
  print(feed)