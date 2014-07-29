#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import transitfeed

from server import config
from server import engine
from server.models import StopSeq
from server.models import Stop
from server.models import Shape
from server.models import Trip

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

Session = sessionmaker(bind=engine)
db = scoped_session(Session)

import server.utils.geom as utils

class TripActions(object):

  def __init__(self, trip_id):
    self.db = db
    trip = db.query(Trip).filter_by(trip_id=trip_id).first()
    stopsSequence = db.query(Stop, StopSeq).\
      join(StopSeq, Stop.stop_id == StopSeq.stop_id).\
      filter(StopSeq.trip_id == trip_id).\
      order_by(StopSeq.stop_sequence).all()
    self.stops = [item.Stop for item in stopsSequence]
    self.shape = db.query(Shape).filter_by(shape_id=trip.shape_id).all()

  def offsetStops(self, offset=6.0):
    self.computeAllSnaps()
    self.stops = []
    for stop,snap in self.snaps:
      nLat = snap['node']['lat']
      nLon = snap['node']['lon']
      of = utils.leftHand(snap['node'], snap['heading'], offset)
      nStop = {'stop_id':stop['stop_id'], 
                'lat':of['lat'],
                'lon':of['lon']}
      self.stops.append(nStop)
    return self

  def computeAllSnaps(self):
    self.snaps = []
    shape_lat_lon = lambda Shape: {
      'lat': Shape.shape_pt_lat, 
      'lon': Shape.shape_pt_lon}
    stop_lat_lon = lambda Stop: {
      'stop_id': Stop.stop_id,
      'lat': Stop.stop_lat,
      'lon': Stop.stop_lon}
    
    shape_dicts = map(shape_lat_lon, self.shape)

    for stop in self.stops:
      stop_dict = stop_lat_lon(stop)
      snap = utils.snapPointToPolygon(stop_dict, shape_dicts)
      self.snaps.append({
        'Stop': stop,
        'Snap': snap
        })
    return self

  def sortStops(self, commit=False):
    """ Compute stop snaps for each stop. Sort according to traveled 
     distance for each snap point. Return a sorted list of stops """
    self.computeAllSnaps()
    sortedStops = sorted(self.snaps, key=lambda StopSnap: StopSnap['Snap']['traveled'])
    assert len(self.stops) == len(sortedStops)
    
    self.stops = [stopSnap['Stop'] for stopSnap in sortedStops]
    return self.stops

  def computeStopDistTraveled(self):
    logger.debug("Updating traveled distance for trip")
    self.computeAllSnaps()
    for s in self.snaps:
        stop_id = s['Stop'].stop_id

        d = "{0:.3f}".format(s['Snap']['traveled'])
        print s['Stop'], d
        
        # q = """UPDATE stop_seq SET shape_dist_traveled='{d}' 
        #     WHERE trip_id='{trip_id}' 
        #     AND stop_id='{stop_id}'""".format(d=d, trip_id=self.trip_id, stop_id=stop_id)
        # self.db.query(q)