#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify
from flask import request
from .. import db
from ..models import Shape
from . import api
import app.services.geojson as geojson

# DEPRECATED
@api.route('/shape/<shape_id>')
def getShape(shape_id):
  shape = db.session.query(Shape).filter(Shape.shape_id == shape_id)\
    .order_by(Shape.shape_pt_sequence).all()
  coords = [[pt.shape_pt_lon,pt.shape_pt_lat] for pt in shape]
  feature = geojson.feature(id=shape_id, feature_type="LineString",
    coords=coords, properties={})
  return jsonify(geojson.featureCollection([feature]))

# DEPRECATED
@api.route('/shape/<shape_id>',  methods=['PUT'])
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

  return jsonify({'success': True,'shape_id': shape_id})


@api.route('/shapes/<shape_id>.json')
def getShapeById(shape_id):
  shape = db.session.query(Shape).filter_by(shape_id=shape_id)\
  	.order_by(Shape.shape_pt_sequence).all()

  return jsonify({
    "shape_id": shape_id,
    "coordinates": [[pt.shape_pt_lon, pt.shape_pt_lat] for pt in shape]
    })


@api.route('/shapes', methods=['POST'])
@api.route('/shapes/', methods=['POST'])
def createShape():
  data = request.json
  coordinates = data.get('coordinates', [])
  shape_id = db.session.query(db.func.max(Shape.shape_id)).scalar() + 1
  for i, pt in enumerate(coordinates):
    d = {
      'shape_id': shape_id,
      'shape_pt_lon': pt[0],
      'shape_pt_lat': pt[1],
      'shape_pt_sequence': i+1
      }
    shape_pt = Shape(**d)
    db.session.add(shape_pt)
  db.session.commit()

  return jsonify({
    'shape_id': shape_id,
    'coordinates': coordinates
    })


@api.route('/shapes/<shape_id>.json', methods=['PUT'])
def updateShapeById(shape_id):
  data = request.json
  coordinates = data.get('coordinates', [])
  db.session.query(Shape).filter_by(shape_id=shape_id).delete()

  for i, pt in enumerate(coordinates):
    d = {
      'shape_id': shape_id,
      'shape_pt_lon': pt[0],
      'shape_pt_lat': pt[1],
      'shape_pt_sequence': i+1
      }
    shape_pt = Shape(**d)
    db.session.add(shape_pt)
  db.session.commit()

  return jsonify({
    'shape_id': shape_id,
    'coordinates': coordinates
    })


@api.route('/shapes/<shape_id>.json', methods=['DELETE'])
def deleteShapeById(shape_id):
  db.session.query(Shape).filter_by(shape_id=shape_id).delete()
  db.session.commit()

  return jsonify({
    'shape_id': shape_id
    })
