#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

class StopSequence(object):

  def __init__(self, trip_id):
    self.db = db
    trip = db.query(Trip).filter_by(trip_id=trip_id).first()
    self.stopsSequence = db.query(Stop, StopSeq).\
      join(StopSeq, Stop.stop_id == StopSeq.stop_id).\
      filter(StopSeq.trip_id == trip_id).\
      order_by(StopSeq.stop_sequence).all()
    self.stops = [item.Stop for item in self.stopsSequence]
    self.shape = db.query(Shape).filter_by(shape_id=trip.shape_id).all()

  def offsetStops(self, offset=6.0):
    raise NotImplementedError
    self.computeAllSnaps()
    for stop, snap in self.snaps:
      nLat = snap['node']['lat']
      nLon = snap['node']['lon']
      of = utils.leftHand(snap['node'], snap['heading'], offset)
      nStop = {'stop_id':stop['stop_id'], 
                'lat':of['lat'],
                'lon':of['lon']}
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

    for item in self.stopsSequence:
      stop = item.Stop
      stop_dict = stop_lat_lon(item.Stop)
      snap = utils.snapPointToPolygon(stop_dict, shape_dicts)
      self.snaps.append({
        'StopSeq': item.StopSeq,
        'Stop': item.Stop,
        'Snap': snap
        })

  def sortStops(self, commit=False):
    """ Compute stop snaps for each stop. Sort according to traveled 
     distance for each snap point. Return a sorted list of stops """
    self.computeAllSnaps()
    sortedStops = sorted(self.snaps, key=lambda StopSnap: StopSnap['Snap']['traveled'])
    for i, item in enumerate(sortedStops):
      stopSeq = item['StopSeq']
      stopSeq.stop_sequence = i + 1
      db.merge(stopSeq)
    db.commit()

  def updateStopSeqDistTraveled(self):
    logger.debug("Updating traveled distance for trip")
    self.computeAllSnaps()
    for s in self.snaps:
      stopSeq = s['StopSeq']
      snap = s['Snap']
      shape_dist_traveled = "{0:.4f}".format(snap['traveled'])
      stopSeq.shape_dist_traveled = shape_dist_traveled
      db.merge(stopSeq)
    db.commit()