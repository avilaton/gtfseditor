#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request
from server import app
import server.geojson as geojson
from server.models import Shape

@app.route('/api/shape/<shape_id>')
def shape(db, shape_id):
  print shape_id
  shape = db.query(Shape).filter(Shape.shape_id == shape_id)\
  	.order_by(Shape.shape_pt_sequence).all()
  coords = [[pt.shape_pt_lon,pt.shape_pt_lat] for pt in shape]
  feature = geojson.feature(id=shape_id, feature_type="Line",
  	coords=coords, properties={})
  return geojson.featureCollection([feature])

# @app.put('/api/shape/<shape_id>')
# def shape(shape_id):
#   geojsonShape = request.json
#   return Shape.set(shape_id, geojsonShape)
