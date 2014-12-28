#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Shape
from . import api


@api.route('/shape/<shape_id>')
def getShape(shape_id):
  logger.info("Shape fetched")
  shape = db.session.query(Shape).filter(Shape.shape_id == shape_id)\
  	.order_by(Shape.shape_pt_sequence).all()
  coords = [[pt.shape_pt_lon,pt.shape_pt_lat] for pt in shape]
  feature = geojson.feature(id=shape_id, feature_type="LineString",
  	coords=coords, properties={})
  return geojson.featureCollection([feature])

@api.put('/shape/<shape_id>')
def updateShape(shape_id):
  geojsonShape = request.json
  for feature in geojsonShape['features']:
    if feature['geometry']['type'] == 'LineString':
      coordList = feature['geometry']['coordinates']
      db.session.query(Shape).filter_by(shape_id = shape_id).delete()
      for i,pt in enumerate(coordList):
        d = {
          'shape_id': shape_id,
          'shape_pt_lon': pt[0],
          'shape_pt_lat': pt[1],
          'shape_pt_sequence': i+1
          }
        shape_pt = Shape(**d)
        db.session.add(shape_pt)

  return {'success': True,'shape_id': shape_id}
