#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from ..models import *

import geom
import transitfeed

class StopSequence(object):

  def __init__(self, trip_id, db):
    self.db = db
    self.trip_id = trip_id
    trip = self.db.session.query(Trip).filter_by(trip_id=trip_id).first()
    self.stopsSequence = self.db.session.query(Stop, StopSeq).\
      join(StopSeq, Stop.stop_id == StopSeq.stop_id).\
      filter(StopSeq.trip_id == trip_id).\
      order_by(StopSeq.stop_sequence).all()
    self.stops = [item.Stop for item in self.stopsSequence]
    self.shape = self.db.session.query(ShapePath).filter_by(shape_id=trip.shape_id).first()

  def offsetStops(self, offset=6.0):
    raise NotImplementedError
    self.computeAllSnaps()
    for stop, snap in self.snaps:
      nLat = snap['node']['lat']
      nLon = snap['node']['lon']
      of = geom.leftHand(snap['node'], snap['heading'], offset)
      nStop = {'stop_id':stop['stop_id'], 
                'lat':of['lat'],
                'lon':of['lon']}
    return self

  def _computeAllSnaps(self):
    self.snaps = []
    stop_lat_lon = lambda Stop: {
      'stop_id': Stop.stop_id,
      'lat': Stop.stop_lat,
      'lon': Stop.stop_lon}

    shape_dicts = self.shape.shape_path_obj_array

    for item in self.stopsSequence:
      stop = item.Stop
      stop_dict = stop_lat_lon(item.Stop)
      snap = geom.snapPointToPolygon(stop_dict, shape_dicts)
      self.snaps.append({
        'StopSeq': item.StopSeq,
        'Stop': item.Stop,
        'Snap': snap
        })

  def sortStops(self, commit=False):
    logger.debug("Sorting stops in trip_id: %s", self.trip_id)
    self._computeAllSnaps()
    sortedStops = sorted(self.snaps, key=lambda StopSnap: StopSnap['Snap']['traveled'])
    for i, item in enumerate(sortedStops):
      stopSeq = item['StopSeq']
      stopSeq.stop_sequence = i + 1
      self.db.session.merge(stopSeq)
    self.db.session.commit()

  def updateDistances(self):
    logger.debug("Updating traveled distance for trip_id: %s", self.trip_id)
    self._computeAllSnaps()
    for s in self.snaps:
      stopSeq = s['StopSeq']
      snap = s['Snap']
      shape_dist_traveled = "{0:.4f}".format(snap['traveled'])
      stopSeq.shape_dist_traveled = shape_dist_traveled
      self.db.session.merge(stopSeq)
    self.db.session.commit()

  def interpolateTimes(self, speed=20, commit=False, n_timepoints=5):
    logger.debug("Interpolating stop times for trip_id: %s", self.trip_id)
    interval = len(self.stopsSequence)/n_timepoints or 1
    for i, item in enumerate(self.stopsSequence):
      stop = item.Stop
      stopSeq = item.StopSeq
      if i % interval == 0 or i + 1 == len(self.stopsSequence):
        dist_traveled = float(stopSeq.shape_dist_traveled)
        stop_time_secs = int(3600*dist_traveled/(speed))
        stop_time = transitfeed.FormatSecondsSinceMidnight(stop_time_secs)
      else:
        stop_time = None
      stopSeq.stop_time = stop_time
      self.db.session.merge(stopSeq)
    self.db.session.commit()
