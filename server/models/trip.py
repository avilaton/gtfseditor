#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Sequence, String, Float, Boolean
from base import Base, Entity

class Trip(Base, Entity):
  __tablename__ = 'trips'
  trip_id = Column(String(50), primary_key=True)
  route_id = Column(String(50))
  service_id = Column(String(50))
  trip_headsign = Column(String(150))
  trip_short_name = Column(String(150))
  direction_id = Column(String(50))
  shape_id = Column(String(50))
  
  def __repr__(self):
    return "<trip: '%s' (trip_short_name:'%s')>" % (self.trip_id, 
      self.trip_short_name)
