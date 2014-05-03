#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server.transitfeededitor import db

class Stop(object):
  """docstring for stops"""
  def __init__(self):
    self.db = db

  def all(self):
    stops = []
    self.db.query("""SELECT * FROM stops WHERE stop_id IN 
      (SELECT DISTINCT stop_id FROM stop_seq)""")
    for r in self.db.cursor.fetchall():
      stops.append(dict(r))
    return stops

  def stops(self):
    stops = []
    self.db.query("""SELECT * FROM stops WHERE stop_id IN 
      (SELECT DISTINCT stop_id FROM stop_seq)""")
    for r in self.db.cursor.fetchall():
      stops.append(dict(r))
    return stops

  def allTrips(self):
    self.db.query("""SELECT trip_id FROM trips""")
    trips = [r['trip_id'] for r in self.db.cursor.fetchall()]
    return trips

  def findStop(self, stop_id):
    data = self.db.select('stops',stop_id=stop_id)
    if data:
      stop = data[0]
      l = self.db.select('stop_seq',stop_id=stop_id)
      lineas = [t['trip_id'] for t in l]
      f = geojson.geoJsonFeature(stop_id,
        stop['stop_lon'], stop['stop_lat'],
        {'stop_id':stop_id,
        'stop_lineas':lineas,
        'stop_calle':stop['stop_calle'],
        'stop_numero':stop['stop_numero'],
        'stop_esquina':stop['stop_esquina'],
        'stop_entre':stop['stop_entre']})
      response = geojson.geoJsonFeatCollection([f])
    else:
      response = {'success': False}
    return response

  def unnamedStops(self):
    self.db.query("""SELECT stop_id FROM stops 
      WHERE 
        stop_id IN (SELECT DISTINCT stop_id FROM stop_seq) 
      AND stop_calle=''""")
    stops = [r['stop_id'] for r in self.db.cursor.fetchall()]
    return stops

  def updateStop(self, stop_id, data):
    """ Stub - should carry out a full update, only updates stop_calle"""
    p = {'stop_id': stop_id}
    p['stop_calle'] = data['properties']['stop_calle'].encode('utf-8')
    p['stop_lon'] = data['geometry']['coordinates'][0]
    p['stop_lat'] = data['geometry']['coordinates'][1]
    result = self.db.query("""UPDATE stops 
      SET stop_calle='{stop_calle}', 
        stop_lat='{stop_lat}', stop_lon='{stop_lon}'
      WHERE stop_id='{stop_id}'"""
      .format(**p))
    self.db.connection.commit()
    return {'success': True, 'result': p}

  def deleteStop(self, stop_id):
    """Deletes a stop by stop_id"""
    result = self.db.query("""DELETE FROM stops WHERE stop_id='{stop_id}'"""
      .format(stop_id=stop_id))
    self.db.connection.commit()
    return {'success': True, 'result': result}
