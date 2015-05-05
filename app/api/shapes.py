#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify
from flask import request
from flask import abort
from .. import db
from ..models import Shape
from ..models import Trip
from . import api
from .decorators import admin_required


@api.route('/shapes/<shape_id>.json')
def getShapeById(shape_id):
  shape = db.session.query(Shape).filter_by(shape_id=shape_id)\
    .order_by(Shape.shape_pt_sequence).all()

  if not shape:
    abort(404, 'shape not found')

  return jsonify({
    "shape_id": shape_id,
    "coordinates": [[pt.shape_pt_lon, pt.shape_pt_lat] for pt in shape]
    })


@api.route('/shapes', methods=['POST'])
@api.route('/shapes/', methods=['POST'])
@admin_required
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
@admin_required
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
@admin_required
def deleteShapeById(shape_id):
  db.session.query(Shape).filter_by(shape_id=shape_id).delete()
  db.session.commit()

  return jsonify({
    'shape_id': shape_id
    })


@api.route('/trips/<trip_id>/shape.json')
def getTripShape(trip_id):
  trip_shape_id = db.session.query(Trip.shape_id).filter_by(trip_id=trip_id).subquery()

  shape = db.session.query(Shape).filter(Shape.shape_id == trip_shape_id)\
    .order_by(Shape.shape_pt_sequence).all()

  if not shape:
    abort(404, 'shape not found')

  return jsonify({
    "shape_id": shape[0].shape_id,
    "coordinates": [[pt.shape_pt_lon, pt.shape_pt_lat] for pt in shape]
    })


@api.route('/trips/<trip_id>/shape.json', methods=['POST'])
@admin_required
def createTripShape(trip_id):
  coordinates = request.json.get('coordinates', [])
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
  trip = db.session.query(Trip).filter_by(trip_id=trip_id).one()
  trip.shape_id = shape_id
  db.session.merge(trip)

  db.session.commit()

  return jsonify({'shape_id': shape_id, 'coordinates': coordinates})


@api.route('/trips/<trip_id>/shape.json', methods=['PUT'])
@admin_required
def updateTripShape(trip_id):
  shape_id = db.session.query(Trip.shape_id).filter_by(trip_id=trip_id).scalar()
  coordinates = request.json.get('coordinates', [])
  db.session.query(Shape).filter_by(shape_id=shape_id).delete()

  for i, pt in enumerate(coordinates):
    shape_pt = Shape(shape_id=shape_id, shape_pt_lon=p[0], shape_pt_lat=p[1],
      shape_pt_sequence=i+1)
    db.session.add(shape_pt)
  db.session.commit()

  return jsonify({'shape_id': shape_id, 'coordinates': coordinates})


@api.route('/trips/<trip_id>/shape.json', methods=['DELETE'])
@admin_required
def deleteTripShape(trip_id):
  trip_shape_id = db.session.query(Trip.shape_id).filter_by(trip_id=trip_id).\
    subquery()
  db.session.query(Shape).filter(Shape.shape_id == trip_shape_id).delete()
  db.session.commit()

  return jsonify({'shape_id': shape_id})
