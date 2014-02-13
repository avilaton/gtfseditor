#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   gtfstools/Trip.py

import utils

class Trip(object):
  """Represents a gtfs trip"""
  offset = 6.0

  def __init__(self,db,trip_id):
    self.trip_id = trip_id
    self.db = db
    self.snaps = []
    self.__fetchFromDb()

  def __repr__(self):
    n = str(len(self.stops))
    r = ' '.join(
      ["trip_id: "+self.trip_id, 
       "\t shape_id: "+self.shape_id, 
       "\t Number of stops: "+n])
    return r

  def __fetchFromDb(self):
    r = self.db.select('trips',trip_id=self.trip_id)[0]
    self.shape_id = r['shape_id']
    self.trip_headsign = r['trip_headsign']
    self.service_id = r['service_id']
    self.stops = []
    self.shape = []
    self.db.query("""SELECT * FROM shapes WHERE shape_id="{0}" 
              ORDER BY shape_pt_sequence""".format(self.shape_id))
    for pt in self.db.cursor.fetchall():
      self.shape.append({'lat':pt['shape_pt_lat'],'lon':pt['shape_pt_lon']})

    self.db.query("""SELECT * FROM stop_seq WHERE trip_id="{0}" 
              ORDER BY stop_sequence""".format(self.trip_id))
    for stop in self.db.cursor.fetchall():
      try:
        stop = self.db.select('stops',stop_id=stop['stop_id'])[0]
        stopDict = {'stop_id':stop['stop_id'],
          'lat':stop['stop_lat'],
          'lon':stop['stop_lon']}
        self.stops.append(stopDict)
      except Exception, e:
        print("unable to find stop: "+stop['stop_id'])

  def saveShapeToDb(self):
    self.db.remove('shapes',shape_id=self.shape_id)
    for i,s in enumerate(self.shape):
      self.db.insert('shapes', 
        shape_id=self.shape_id,
        shape_pt_lat=s['lat'],
        shape_pt_lon=s['lon'],
        shape_pt_sequence=i+1)
    return self

  def saveStopsToDb(self):
    self.db.remove('stop_seq',trip_id=self.trip_id)
    for i,stop in enumerate(self.stops):
      self.db.insert('stop_seq', 
        trip_id=self.trip_id, 
        stop_id=stop['stop_id'], 
        stop_sequence=i+1)
      self.db.update('stops', where={'stop_id':stop['stop_id']},
        data={'stop_lat':stop['lat'], 'stop_lon':stop['lon']})

  def reverseShape(self):
    self.shape.reverse()
    return self

  def offsetStops(self):
    self.computeAllSnaps()
    self.stops = []
    for stop,snap in self.snaps:
      nLat = snap['node']['lat']
      nLon = snap['node']['lon']
      of = utils.leftHand(snap['node'],snap['heading'],Trip.offset)
      nStop = {'stop_id':stop['stop_id'], 
                'lat':of['lat'],
                'lon':of['lon']}
      self.stops.append(nStop)
    return self

  def computeAllSnaps(self):
    self.snaps = []
    for i,stop in enumerate(self.stops):
      snap = self.findStopSnap(stop)
      self.snaps.append([stop,snap])
    return self

  def findStopSnap(self,stop):
    allInterpolators = []
    allCorners = []
    accumulated = 0
    for i in range(len(self.shape)-1):
      # find nearest corner node
      p1 = self.shape[i]
      p2 = self.shape[i+1]
      heading = utils.headingC(p1,p2)
      length = utils.tripLength([p1,p2])
      d1 = utils.haversineDict(stop,p1)
      d2 = utils.haversineDict(stop,p2)
      cornerSol = {'heading':heading}
      if d1 <= d2:
        cornerSol.update({'node':p1,'dist':d1,'traveled':accumulated})
      else:
        cornerSol.update({'node':p2,'dist':d2,'traveled':accumulated + length})
      allCorners.append(cornerSol)

      b,n = utils.mPoint(p1, p2, stop)
      if b:
        mSol = {'heading':heading, 
          'node': n, 
          'dist':utils.haversineDict(stop,n), 
          'traveled': accumulated + utils.tripLength([p1,n])}
        allInterpolators.append(mSol)    

      accumulated += length

    nearestCorner = min(allCorners,key=lambda x:x['dist'])
    if allInterpolators:
      nearestInterpolator = min(allInterpolators,key=lambda x:x['dist'])
    else:
      nearestInterpolator = []

    if nearestInterpolator:
      if nearestInterpolator['dist'] <= nearestCorner['dist']:
        snap = nearestInterpolator
      else:
        snap = nearestCorner
    else:
      snap = nearestCorner

    return snap

  def refineRoute(nodeList):
    """
    Input is a list of dicts having lon and lat, 
    Output is a list, posibly larger, where points are added linearly 
    interpolating between each pair of points of the input list where 
    the separation excedes a certain value.
    """
    pass

  def sortStops(self):
    """ Compute stop snaps for each stop. Sort according to traveled 
     distance for each snap point. Return a sorted list of stops """
    self.computeAllSnaps()
    sortedStops = sorted(self.snaps, key=lambda x:x[1]['traveled'])
    assert len(self.stops) == len(sortedStops)
    
    self.stops = [i[0] for i in sortedStops]
    return self


def tests(db):

  trip = Trip(db,'N4.ida')
  trip.offsetStops().saveStopsToDb()
  return

if __name__ == '__main__':
  try:
    import ormgeneric as o
    storeDb = 'dbRecorridos.sqlite'
    db = o.dbInterface(storeDb)
    tests(db)
    db.close()
  except ImportError:
    print "ormgeneric is needed to run"
