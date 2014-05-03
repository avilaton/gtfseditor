#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server.transitfeededitor import db as current_db

class Route(object):
  """docstring for stops"""
  db = current_db

  def __init__(self):
    self.db = current_db

  def get(self, route_id):
    return self.db.select('trips',route_id=route_id)

  def trips(self, route_id):
    trips = []
    for row in self.db.select('trips',route_id=route_id):
      trips.append({
        'service_id':row['service_id'],
        'trip_id':row['trip_id'],
        'trip_headsign':row['trip_headsign'],
        'trip_short_name':row['trip_short_name'],
        'direction_id':row['direction_id'],
        'shape_id':row['shape_id']
        })
    return {'trips':trips}

  @classmethod
  def all(cls):
    routes = []
    cls.db.query("""SELECT * FROM routes ORDER BY route_short_name""")
    for row in cls.db.cursor.fetchall():
      data = {}
      for k in ['route_id', 'agency_id', 'route_short_name', 
        'route_long_name', 'route_desc', 'route_type', 
        'route_color']:
        data.update({k:row[k]})
        data['active'] = bool(row['active'])
      routes.append(data)
    return {'routes': routes}
