#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request
from server import app
from server.models import Trip
from server.models import Stop
from server.models import StopSeq

@app.get('/api/trip/<trip_id>/stops')
def tripStops(db, trip_id):
  sequence = db.query(Stop, StopSeq).filter(StopSeq.trip_id == trip_id)\
    .order_by(StopSeq.stop_sequence).all()
  # for stop in sequence:
  #   print stop

  return "ok"

# @put('/api/trip/<trip_id>/stops')
# def saveTripStops(trip_id):
#   if 'q' in request.query:
#     if request.query['q'] == 'sort':
#       result = tb.sortTripStops(trip_id)
#     elif request.query['q'] == 'align':
#       result = tb.alignTripStops(trip_id)
#   else:
#     geojsonTrip = request.json  
#     result = tb.saveTripStops(trip_id, geojsonTrip)
#   return result

# @get('/api/trip/<trip_id>/stop/<stop_id>/timepoint')
# def is_timepoint(trip_id, stop_id):
#   # trip = Trip(trip_id)
#   # stop = trip.stop(stop_id)
#   trip_stop = tb.getTripStop(trip_id, stop_id)
#   return {'is_timepoint': trip_stop['is_timepoint']}

# @put('/api/trip/<trip_id>/stop/<stop_id>/timepoint')
# def set_timepoint(trip_id,stop_id):
#   is_timepoint = request.params.is_timepoint
#   return tb.set_timepoint(trip_id, stop_id, is_timepoint)
