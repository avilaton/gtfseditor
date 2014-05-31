#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Float
from server import Base

class Shape(Base):
  __tablename__ = 'shapes'
  shape_id = Column(String(50), primary_key=True)
  shape_pt_lat = Column(Float(precision=64))
  shape_pt_lon = Column(Float(precision=64))
  shape_pt_sequence = Column(Integer, primary_key=True)

  def __repr__(self):
    return "<Shape_point: (shape_id:'%s', shape_pt_sequence:'%s')>" % (self.shape_id, 
      self.shape_pt_sequence)

  @property
  def as_dict(self):
    d = {}
    for column in self.__table__.columns:
      d[column.name] = unicode(getattr(self, column.name))
    return d





current_db = ''

class ShapeOld(object):
  """docstring for stops"""
  db = current_db

  def __init__(self):
    self.db = current_db

  @classmethod
  def get(self, shape_id):
    result = self.db.select('shapes',shape_id=shape_id)
    coordList = [[p['shape_pt_lon'],p['shape_pt_lat']] for p in result]
    feature = geojson.geoJsonLineString(shape_id,coordList,{'type':'Line'})
    return geojson.geoJsonFeatCollection([feature])

  @classmethod
  def set(self, shape_id, data):
    for feature in data['features']:
      if feature['geometry']['type'] == 'LineString':
        coordList = feature['geometry']['coordinates']
        shape_id = feature['id']
        self.db.remove('shapes',shape_id=shape_id)
        for i,pt in enumerate(coordList):
          self.db.insert('shapes',shape_id=shape_id,
            shape_pt_lat=pt[1],
            shape_pt_lon=pt[0],
            shape_pt_sequence=i+1)
        response = {'success': True,'shape_id': shape_id, 
          'shape': self.shape(shape_id)}
      else:
        response = {'success': False}
    self.db.connection.commit()
    return response
