#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Float
from server import Base

class Shape(Base):
  __tablename__ = 'shapes'
  shape_id = Column(String(50), primary_key=True)
  shape_pt_lat = Column(Float(precision=53))
  shape_pt_lon = Column(Float(precision=53))
  shape_pt_time = Column(String(50))
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
