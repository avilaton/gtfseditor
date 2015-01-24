#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app,make_response
from .. import db
from ..services.feed import Feed
from . import api

@api.route('/feed/')
@api.route('/feed/google_transit.zip')
def index():
  feed = Feed(db = db.session)
  fin = feed.build()
  response = make_response()
  response.headers['Content-Type'] = 'application/zip'
  response.headers['Content-Disposition'] = 'attachment; filename="{0}"'.format(feed.filename)
  return response
