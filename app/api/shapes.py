#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import jsonify
from flask import request
from flask import abort
from .. import db
from ..models import ShapePath
from ..models import Trip
from . import api
from .decorators import admin_required
from .errors import not_found


# DEPRECATED
import app.services.geojson as geojson
@api.route('/shape/<shape_id>.geojson')
def getShape(shape_id):
  shape = ShapePath.query.get(shape_id)
  feature = geojson.feature(id=shape_id, feature_type="LineString",
    coords=shape.shape_path_array, properties={})
  return jsonify(geojson.featureCollection([feature]))


@api.route('/shapes/<shape_id>.json')
def getShapeById(shape_id):
  shape = ShapePath.query.get(shape_id)

  if not shape:
    abort(404, 'shape not found')

  return jsonify({
    "shape_id": shape_id,
    "coordinates": shape.shape_path_array
    })


@api.route('/shapes', methods=['POST'])
@api.route('/shapes/', methods=['POST'])
@admin_required
def createShape():
  data = request.json
  coordinates = data.get('coordinates', [])
  shape = ShapePath(shape_path=json.dumps(coordinates))
  db.session.add(shape)
  db.session.commit()

  return jsonify({
    'shape_id': shape.shape_id,
    'coordinates': shape.shape_path_array
    })


@api.route('/shapes/<shape_id>.json', methods=['PUT'])
@admin_required
def updateShapeById(shape_id):
  coordinates = request.json.get('coordinates', [])

  shape = ShapePath.query.get(shape_id)
  shape.shape_path = json.dumps(coordinates)
  db.session.merge(shape)
  db.session.commit()

  return jsonify({
    'shape_id': shape_id,
    'coordinates': coordinates
    })


@api.route('/shapes/<shape_id>.json', methods=['DELETE'])
@admin_required
def deleteShapeById(shape_id):
  ShapePath.query.get(shape_id).delete()
  db.session.commit()

  return jsonify({
    'shape_id': shape_id
    })


@api.route('/trips/<trip_id>/shape.json')
def getTripShape(trip_id):
  shape_id = db.session.query(Trip.shape_id).filter_by(trip_id=trip_id).scalar()

  shape = ShapePath.query.get(shape_id)

  if not shape:
    abort(404, 'shape not found')

  return jsonify({
    "shape_id": shape_id,
    "coordinates": shape.shape_path_array
    })


@api.route('/trips/<trip_id>/shape.json', methods=['POST'])
@admin_required
def createTripShape(trip_id):
  coordinates = request.json.get('coordinates', [])

  shape = ShapePath(shape_path=json.dumps(coordinates))
  db.session.add(shape)

  trip = db.session.query(Trip).filter_by(trip_id=trip_id).one()
  trip.shape_id = shape.shape_id
  db.session.merge(trip)
  db.session.commit()

  return jsonify({'shape_id': shape.shape_id, 'coordinates': coordinates})


@api.route('/trips/<trip_id>/shape.json', methods=['PUT'])
@admin_required
def updateTripShape(trip_id):
  coordinates = request.json.get('coordinates', [])

  shape_id = db.session.query(Trip.shape_id).filter_by(trip_id=trip_id).scalar()
  shape = ShapePath.query.get(shape_id)

  shape.shape_path = json.dumps(coordinates)
  db.session.merge(shape)
  db.session.commit()

  return jsonify({'shape_id': shape_id, 'coordinates': coordinates})


@api.route('/trips/<trip_id>/shape.json', methods=['DELETE'])
@admin_required
def deleteTripShape(trip_id):
  try:
    trip = db.session.query(Trip).filter_by(trip_id=trip_id).one()
  except Exception, e:
    return not_found('trip does not exist')

  ShapePath.query.filter_by(shape_id=trip.shape_id).delete()
  trip.shape_id = None
  db.session.merge(trip)
  db.session.commit()

  return jsonify({'shape_id': trip.shape_id})
