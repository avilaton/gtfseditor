#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from bottle import request
from server import app
import server.geojson as geojson
from server.models import Shape

@app.route('/api/shape/<shape_id>')
def getShape(db, shape_id):
  logger.info("Shape fetched")
  shape = db.query(Shape).filter(Shape.shape_id == shape_id)\
  	.order_by(Shape.shape_pt_sequence).all()
  coords = [[pt.shape_pt_lon,pt.shape_pt_lat] for pt in shape]
  feature = geojson.feature(id=shape_id, feature_type="LineString",
  	coords=coords, properties={})
  return geojson.featureCollection([feature])

@app.put('/api/shape/<shape_id>')
def updateShape(db, shape_id):
  geojsonShape = request.json
  for feature in geojsonShape['features']:
    if feature['geometry']['type'] == 'LineString':
      coordList = feature['geometry']['coordinates']
      db.query(Shape).filter_by(shape_id = shape_id).delete()
      for i,pt in enumerate(coordList):
        d = {
          'shape_id': shape_id,
          'shape_pt_lon': pt[0],
          'shape_pt_lat': pt[1],
          'shape_pt_sequence': i+1
          }
        shape_pt = Shape(**d)
        db.add(shape_pt)

  return {'success': True,'shape_id': shape_id}
