#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Sequence, String, Float, Boolean
from server import Base

class Trip(Base):
  __tablename__ = 'trips'
  trip_id = Column(String(50), primary_key=True)
  route_id = Column(String(50))
  service_id = Column(String(50))
  trip_headsign = Column(String(50))
  trip_short_name = Column(String(50))
  direction_id = Column(String(50))
  shape_id = Column(String(50))
  
  def __repr__(self):
    return "<trip: '%s' (trip_short_name:'%s')>" % (self.trip_id, 
      self.trip_short_name)

  @property
  def as_dict(self):
    d = {}
    for column in self.__table__.columns:
      d[column.name] = unicode(getattr(self, column.name))
    return d


import server.gtfstools

from collections import defaultdict

current_db = ''

class TripOld(object):
  """docstring for stops"""
  db = current_db

  def __init__(self, trip_id):
    self.db = current_db
    self.trip_id = trip_id

  def stops(self):
    trip_id = self.trip_id
    features = []
    stopCodes = []
    q = """SELECT stop_id,is_timepoint 
      FROM stop_seq WHERE trip_id='{0}'
      ORDER BY stop_sequence""".format(trip_id)
    self.db.query(q)
    for i,row in enumerate(self.db.cursor.fetchall()):
      stopCodes.append([i,row['stop_id'],row['is_timepoint']])

    for i,stop_id,is_timepoint in stopCodes:
      try:
        d = self.db.select('stops',stop_id=stop_id)[0]
      except Exception, e:
        print("unable to find stop: " + stop_id)
        # raise e
        continue
      l = self.db.select('stop_seq',stop_id=stop_id)
      lineas = [t['trip_id'] for t in l]
      f = geojson.geoJsonFeature(stop_id,
        d['stop_lon'],
        d['stop_lat'],
        {'stop_id':d['stop_id'],
        'stop_seq':i+1,
        'is_timepoint':bool(is_timepoint),
        'stop_lineas':lineas,
        'stop_calle':d['stop_calle'],
        'stop_numero':d['stop_numero'],
        'stop_esquina':d['stop_esquina'],
        'stop_entre':d['stop_entre']})
      features.append(f)
    return geojson.geoJsonFeatCollection(features)

  def stop(self, stop_id):
    return self.db.select('stop_seq', trip_id=self.trip_id,stop_id=stop_id)[0]

  def set_timepoint(self, trip_id, stop_id, is_timepoint):
    q = """UPDATE stop_seq 
        SET is_timepoint={is_timepoint}
        WHERE stop_id='{stop_id}' 
          AND trip_id='{trip_id}'
      """.format(trip_id=trip_id, stop_id=stop_id, 
        is_timepoint=is_timepoint)
    self.db.query(q)
    return {'is_timepoint': is_timepoint}

  def saveTripStops(self, trip_id, data):
    stops = data
    self.db.remove('stop_seq',trip_id=trip_id)
    featureList = stops['features']
    
    # create new ids for new stops
    for i,f in enumerate(featureList):
      p = defaultdict(str)
      for k,v in f['properties'].items():
        p[k] = v

      if 'id' in f:
        stop_id = f['id']
        stop_seq = p['stop_seq']
      else:
        stop_id = self.getNewStopId()
        stop_seq = 1000+i

      self.db.insert('stop_seq',trip_id=trip_id,stop_id=stop_id,stop_sequence=stop_seq)
      
      stop_lon,stop_lat = f['geometry']['coordinates']

      # do not save stops while saving trip. only save trip members. 2014-02-16
      # self.db.insert('stops',stop_id=stop_id,
      #   stop_lat=stop_lat,
      #   stop_lon=stop_lon,
      #   stop_calle = p['stop_calle'],
      #   stop_entre = p['stop_entre'],
      #   stop_numero = p['stop_numero']
      #   )

    # self.tripStops(trip_id)
    self.db.connection.commit()

    return {'success':True,'trip_id':trip_id, 'stops':self.tripStops(trip_id)}

  def sortTripStops(self, trip_id):
    print("Sorting stops along trip:\t" + trip_id)
    trip = gtfstools.Trip(self.db, trip_id)
    trip.sortStops().saveStopsToDb()
    self.commit()
    return {'success': True}

  def updateTripDistTraveled(self, trip_id):
    print("Updating traveled distance for trip:\t" + trip_id)
    tripTb = gtfstools.Trip(self.db, trip_id)
    tripTb.computeAllSnaps()
    for s in tripTb.snaps:
        stop_id = s[0]['stop_id']
        d = "{0:.3f}".format(s[1]['traveled'])
        # print stop_id, d
        q = """UPDATE stop_seq SET shape_dist_traveled='{d}' 
            WHERE trip_id='{trip_id}' 
            AND stop_id='{stop_id}'""".format(d=d, trip_id=trip_id, stop_id=stop_id)
        self.db.query(q)
  
  def alignTripStops(self, trip_id):
    trip = gtfstools.Trip(self.db, trip_id)
    trip.offsetStops().saveStopsToDb()
    return {'success': True}
