#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from base import Base, Entity

class TripStartTime(Base, Entity):
  __tablename__ = 'trips_start_times'
  trip_id = Column(String(50), ForeignKey("trips.trip_id"), primary_key=True)
  service_id = Column(String(50), ForeignKey("calendar.service_id"), primary_key=True)
  start_time = Column(String(50), primary_key=True)