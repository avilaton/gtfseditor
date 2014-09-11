#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, ForeignKey
from base import Base, Entity

class Frequency(Base, Entity):
  __tablename__ = 'frequencies'
  trip_id = Column(String(50), ForeignKey("trips.trip_id"), primary_key=True)
  start_time = Column(String(50))
  end_time = Column(String(50))
  headway_secs = Column(String(50))
  exact_times = Column(String(50))
