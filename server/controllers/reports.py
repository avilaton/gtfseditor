#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import StringIO

from bottle import request, response, view, template
from server import app
from server.models import Stop
from server.models import StopSeq
from server.models import Trip
from sqlalchemy import func

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

@app.route('/api/reports/trips.csv')
def trips(db):
  headers = ['trip_id', 'length']
  tripsFile = StringIO.StringIO()
  writer = csv.DictWriter(tripsFile, headers)
  writer.writeheader()
  for row in db.query(StopSeq.trip_id, func.max(StopSeq.shape_dist_traveled)).\
    group_by(StopSeq.trip_id).all():
    writer.writerow({
      'trip_id': row.trip_id, 
      'length': row[1]
      })
  response.set_header('Content-Type', 'text/plain')

  return tripsFile.getvalue()