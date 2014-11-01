#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from base import Base, Entity

class StopTime(Base, Entity):
  __tablename__ = 'stop_times'
  trip_id = Column(String(50), ForeignKey("trips.trip_id"), primary_key=True)
  stop_id = Column(String(50), ForeignKey("stops.stop_id"), primary_key=True)
  stop_sequence = Column(Integer, primary_key=True)
  arrival_time = Column(String(50))
  departure_time = Column(String(50))
  shape_dist_traveled = Column(Float(precision=53))
