#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import ServerTestCase
from server.models import Trip, Stop, StopSeq

class tripModelTest(ServerTestCase):
  def testData(self):
    trip_id = '18.ida'
    sequence = self.db.query(Stop).join(StopSeq, Stop.stop_id == StopSeq.stop_id)\
      .filter(StopSeq.trip_id == trip_id)\
      .order_by(StopSeq.stop_sequence).all()
    self.assertEqual(1,1)

  def testGeoJSON(self):
    trip_id = '18.ida'
    rows = self.db.query(Stop, StopSeq).join(StopSeq, Stop.stop_id == StopSeq.stop_id)\
      .filter(StopSeq.trip_id == trip_id)\
      .order_by(StopSeq.stop_sequence).all()

    from server import geojson
    features = []

    for row in rows:
      stop = row.Stop
      stop_seq = row.StopSeq
      properties = stop.as_dict
      properties.update({'stop_seq': stop_seq.stop_sequence})
      f = geojson.feature(id = stop.stop_id,
        coords = [stop.stop_lon, stop.stop_lat], 
        properties = properties)
      features.append(f)
    print geojson.featureCollection(features)
