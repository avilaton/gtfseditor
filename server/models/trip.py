#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, String
from base import Base, Entity

class Trip(Base, Entity):
  __tablename__ = 'trips'
  trip_id = Column(String(50), primary_key=True)
  route_id = Column(String(50), ForeignKey("routes.route_id"))
  service_id = Column(String(50), ForeignKey("calendar.service_id"))
  trip_headsign = Column(String(150))
  trip_short_name = Column(String(150))
  direction_id = Column(String(50))
  shape_id = Column(String(50))
