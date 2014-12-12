#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request, abort, static_file, response
from server import app
from server.services.feed import Feed

@app.route('/api/feed/')
@app.route('/api/feed/google_transit.zip')
def index(db):
  feed = Feed()
  fin = feed.build()

  response.content_type = 'application/zip'
  response.set_header('Content-Disposition', 
    'attachment; filename="{0}"'.format(feed.filename))
  return fin.getvalue()
