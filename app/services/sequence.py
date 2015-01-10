#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from ..models import *

import server.utils.geom as utils
import transitfeed

class StopSequence(object):

  def __init__(self, trip_id):
    self.db = db
    self.trip_id = trip_id
    trip = db.session.query(Trip).filter_by(trip_id=trip_id).first()
    self.stopsSequence = db.session.query(Stop, StopSeq).\
      join(StopSeq, Stop.stop_id == StopSeq.stop_id).\
      filter(StopSeq.trip_id == trip_id).\
      order_by(StopSeq.stop_sequence).all()
    self.stops = [item.Stop for item in self.stopsSequence]
    self.shape = db.session.query(Shape).filter_by(shape_id=trip.shape_id).all()

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

  def _computeAllSnaps(self):
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
    logger.debug("Sorting stops in trip_id: %s", self.trip_id)
    self._computeAllSnaps()
    sortedStops = sorted(self.snaps, key=lambda StopSnap: StopSnap['Snap']['traveled'])
    db.session.query(StopSeq).filter_by(trip_id = self.trip_id).delete()
    for i, item in enumerate(sortedStops):
      stopSeq = item['StopSeq']
      stopSeq.stop_sequence = i + 1
      db.session.merge(stopSeq)
    db.session.commit()

  def updateDistances(self):
    logger.debug("Updating traveled distance for trip_id: %s", self.trip_id)
    self._computeAllSnaps()
    for s in self.snaps:
      stopSeq = s['StopSeq']
      snap = s['Snap']
      shape_dist_traveled = "{0:.4f}".format(snap['traveled'])
      stopSeq.shape_dist_traveled = shape_dist_traveled
      db.session.merge(stopSeq)
    db.session.commit()

  def interpolateTimes(self, speed=20, commit=False):
    logger.debug("Interpolating stop times for trip_id: %s", self.trip_id)
    for item in self.stopsSequence:
      stop = item.Stop
      stopSeq = item.StopSeq
      dist_traveled = float(stopSeq.shape_dist_traveled)
      stop_time_secs = int(3600*dist_traveled/(speed))
      stop_time = transitfeed.FormatSecondsSinceMidnight(stop_time_secs)
      stopSeq.stop_time = stop_time
      db.session.merge(stopSeq)
    db.session.commit()
