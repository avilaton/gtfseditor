#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request, response, view
from server import app
from server.models import Stop

@app.route('/api/reports/unnamed')
@view('unnamed')
def unnamed():
  unnamed = Stop.unnamed()
  return dict(stops=unnamed)

@app.route('/api/reports/available')
@view('available')
def unnamed():
  available = Stop.availableIds()
  return dict(available=available)

@app.route('/api/reports/stop/<stop_id>')
def index(db, stop_id):
  stops = db.query(Stop).all()
  # for stop in stops:
  #   print stop
  return template('stops.html', stop_id=stop_id, stops=stops)
