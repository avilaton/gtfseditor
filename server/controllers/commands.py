#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route
# remove this global latter on
from server.transitfeededitor import tb

@route('/api/commands/<command>/<param>')
def dataSetCommands(command, param):
  results = []
  print param
  if command == 'sort':
    if param != '*':
      print("sorting trip: "+param)
      results.append(tb.sortTripStops(param))
      return {'results': results}
    else:
      trips = tb.allTrips()
      for trip_id in trips:
        print("sorting trip: "+trip_id)
        results.append(tb.sortTripStops(trip_id))
      return {'results': results, 'trips': trips}
  elif command == offset:
    pass
