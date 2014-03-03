#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtfstools
import geojson
from collections import defaultdict
# import xml
import gtfstools

class Stops(object):
  """docstring for stops"""
  def __init__(self, db):
    self.db = db

  def all(self):
    stops = []
    self.db.query("""SELECT * FROM stops WHERE stop_id IN 
      (SELECT DISTINCT stop_id FROM stop_seq)""")
    for r in self.db.cursor.fetchall():
      stops.append(dict(r))
    return stops
    

class toolbox(object):
  def __init__(self, db):
    self.db = db
    self.Stops = Stops(db)

  def commit(self):
    self.db.connection.commit()

  ################
  # stops
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

  ################
  # routes
  def routes(self):
    routes = []
    self.db.query("""SELECT * FROM routes ORDER BY route_short_name""")

    for row in self.db.cursor.fetchall():
      data = {}
      for k in ['route_id', 'agency_id', 'route_short_name', 
        'route_long_name', 'route_desc', 'route_type', 
        'route_color']:
        data.update({k:row[k]})
        data['active'] = bool(row['active'])
      routes.append(data)
    return {'routes': routes}

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

  def shape(self, shape_id):
    result = self.db.select('shapes',shape_id=shape_id)
    coordList = [[p['shape_pt_lon'],p['shape_pt_lat']] for p in result]
    feature = geojson.geoJsonLineString(shape_id,coordList,{'type':'Line'})
    return geojson.geoJsonFeatCollection([feature])

  def tripStops(self, trip_id):
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

  def bbox(self, bbox, filterQ):
    w,s,e,n = map(float,bbox.split(','))
    q = ["""SELECT * 
        FROM stops s INNER JOIN stop_seq sq ON s.stop_id=sq.stop_id
        WHERE
          (stop_lat BETWEEN {s} AND {n})
          AND 
          (stop_lon BETWEEN {w} AND {e}) """]

    if filterQ:
      if 'id:' in filterQ:
        stop_id = filterQ.split(':')[1]
        q.append("""AND s.stop_id='{f}'""")
        q.append("LIMIT 300")
        query = ''.join(q).format(s=s,n=n,w=w,e=e, f=stop_id)
      elif 'calle:' in filterQ:
        stop_calle = filterQ.split(':')[1]
        q.append("""AND s.stop_calle LIKE '%{f}%'""")
        q.append("LIMIT 300")
        query = ''.join(q).format(s=s,n=n,w=w,e=e, f=stop_calle)
      else:
        q.append("""AND s.stop_calle LIKE '%{f}%'""")
        q.append("LIMIT 300")
        query = ''.join(q).format(s=s,n=n,w=w,e=e, f=filterQ)
    else:
      q.append("LIMIT 300")
      query = ''.join(q).format(s=s,n=n,w=w,e=e)
    self.db.query(query)

    d = {}
    for r in self.db.cursor.fetchall():
      stop = dict(r)
      linea = stop.pop('trip_id')
      stop_id = stop.pop('stop_id')
      if stop_id in d:
        d[stop_id]['lineas'].append(linea)
      else:
        d[stop_id] = stop
        d[stop_id]['lineas'] = [linea]
    
    features = []
    for stop_id,stop in d.items():
      f = geojson.geoJsonFeature(stop_id,
        stop['stop_lon'],
        stop['stop_lat'],
        {'stop_id':stop_id,
        'stop_lineas':stop['lineas'],
        'stop_calle':stop['stop_calle'],
        'stop_numero':stop['stop_numero'],
        'stop_esquina':stop['stop_esquina'],
        'stop_entre':stop['stop_entre']})
      features.append(f)
    return geojson.geoJsonFeatCollection(features)

  def getTripStop(self, trip_id, stop_id):
    return db.select('stop_seq', trip_id=trip_id,stop_id=stop_id)[0]

  def set_timepoint(self, trip_id, stop_id, is_timepoint):
    q = """UPDATE stop_seq 
        SET is_timepoint={is_timepoint}
        WHERE stop_id='{stop_id}' 
          AND trip_id='{trip_id}'
      """.format(trip_id=trip_id, stop_id=stop_id, 
        is_timepoint=is_timepoint)
    self.db.query(q)
    return {'is_timepoint': is_timepoint}

  def availableStopIds(self):
    self.db.query("""SELECT stop_id FROM stops""")
    allIds = set(range(1,10000))
    usedIds = [int(r['stop_id'][1:]) for r in self.db.cursor.fetchall()]
    availableIds = allIds.difference(usedIds)
    print(len(availableIds))
    print(len(usedIds))
    return availableIds

  def getNewStopId(self):
    self.db.query("""SELECT stop_id FROM stops""")
    ids = [int(row['stop_id'][1:]) for row in self.db.cursor.fetchall()]
    newId = 'C'+str(max(ids)+1)
    return newId

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

  def saveShape(self, shape_id, data):
    for feature in data['features']:
      if feature['geometry']['type'] == 'LineString':
        coordList = feature['geometry']['coordinates']
        shape_id = feature['id']
        self.db.remove('shapes',shape_id=shape_id)
        for i,pt in enumerate(coordList):
          self.db.insert('shapes',shape_id=shape_id,
            shape_pt_lat=pt[1],
            shape_pt_lon=pt[0],
            shape_pt_sequence=i+1)
        response = {'success': True,'shape_id': shape_id, 
          'shape': self.shape(shape_id)}
      else:
        response = {'success': False}
    self.db.connection.commit()
    return response

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

  def constructStopNames(self):
      self.db.query("""SELECT * FROM stops WHERE stop_id IN 
          (SELECT DISTINCT stop_id FROM stop_seq)""")

      for stop in self.db.cursor.fetchall():
          lat = stop['stop_lat']
          lng = stop['stop_lon']
          if stop['stop_calle']:
              if stop['stop_numero']:
                  name = stop['stop_calle'] + ' ' + str(stop['stop_numero'])
              else:
                  if stop['stop_entre']:
                      if ' y ' in stop['stop_entre']:
                          name = stop['stop_calle'] + u' entre ' + stop['stop_entre']
                      else:
                          name = stop['stop_calle'] + u', ' + stop['stop_entre']
                  else:
                      name = stop['stop_calle']
          else:
              if type(stop['stop_id']) is int:
                  name = str(stop['stop_id'])
              name = str(stop['stop_id'])
              name = name.zfill(4)
          self.db.query("""UPDATE stops SET stop_name='{name}' 
              WHERE stop_id='{stop_id}' """.format(name=name.encode('utf-8'), stop_id=stop['stop_id']))
  
  def updateDistTraveled(self):
    """DEPRECATED, use updateTripDistTraveled """
    self.db.query("""SELECT DISTINCT trip_id FROM stop_seq""")
    for row in self.db.cursor.fetchall():
      trip_id = row["trip_id"]
      print "updating traveled distance for trip:", trip_id
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

  def fakeFrequencyTable(self):
    self.db.query("SELECT trip_id FROM trips")
    for r in self.db.cursor.fetchall():
      trip_id = r['trip_id']
      self.db.query("""DELETE * FROM frequencies""")
      self.db.insert('frequencies', 
          trip_id=trip_id, 
          start_time="08:00:00", 
          end_time="23:59:59",
          headway_secs=900,
          exact_times=0)


if __name__ == '__main__':
  import ormgeneric as o
  db = o.dbInterface('dbRecorridos.sqlite')
  tb = toolbox(db)
  print tb.shape('A0.ida')
  print tb.findStop('C0004')
