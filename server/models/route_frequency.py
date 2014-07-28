#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Float
from base import Base, Entity

class RouteFrequency(Base, Entity):
  __tablename__ = 'route_frequencies'
  route_id = Column(String(50), primary_key=True)
  service_id = Column(String(50), primary_key=True)
  start_time = Column(String(50), primary_key=True)
  end_time = Column(String(50), primary_key=True)
  headway_secs = Column(Integer)
