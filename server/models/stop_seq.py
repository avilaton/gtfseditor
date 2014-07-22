#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Float
from base import Base, Entity

class StopSeq(Base, Entity):
  __tablename__ = 'stop_seq'
  trip_id = Column(String(50), primary_key=True)
  stop_id = Column(String(50), primary_key=True)
  stop_sequence = Column(Integer, primary_key=True) 
  stop_time = Column(String(50)) 
  shape_dist_traveled = Column(Float(precision=53))
  # is_timepoint = Column(String(50), default="FALSE")

  def __repr__(self):
    return "<Stop_seq for trip: '%s' (stop_id:'%s', stop_sequence:'%s')>" % (self.trip_id, 
      self.stop_id, self.stop_sequence)
