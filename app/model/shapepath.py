#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from app import db
from .entity import Entity


class ShapePath(db.Model, Entity):
  __tablename__ = 'shape_paths'
  shape_id = db.Column(db.Integer, primary_key=True)
  shape_path = db.Column(db.UnicodeText) # Stores json Array of Lon, Lat pairs

  @property
  def shape_path_array(self):
    return json.loads(self.shape_path)

  @property
  def shape_path_obj_array(self):
    shape_lat_lon = lambda pt: {'lon': pt[0], 'lat': pt[1]}
    array = json.loads(self.shape_path)
    return map(shape_lat_lon, array)
