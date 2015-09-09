#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class Shape(db.Model, Entity):
  __tablename__ = 'shapes'
  shape_id = db.Column(db.Integer, primary_key=True)
  shape_pt_lat = db.Column(db.Float(precision=53))
  shape_pt_lon = db.Column(db.Float(precision=53))
  shape_pt_time = db.Column(db.String(50))
  shape_pt_sequence = db.Column(db.Integer, primary_key=True)

  @classmethod
  def vertices(cls, shape_id):
    return db.session.query(cls)\
      .filter(cls.shape_id == shape_id)\
      .order_by(cls.shape_pt_sequence)

  @classmethod
  def get_vertices_array(cls, shape_id):
    return [[pt.shape_pt_lon, pt.shape_pt_lat] for pt in cls.vertices(shape_id).all()]
