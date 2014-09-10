#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, ForeignKey
from base import Base, Entity

class Route(Base, Entity):
  __tablename__ = 'routes'
  route_id = Column(String(50), primary_key=True)
  agency_id = Column(String(50), ForeignKey("agency.agency_id"))
  route_short_name = Column(String(50))
  route_long_name = Column(String(150))
  route_desc = Column(String(150))
  route_type = Column(String(50))
  route_color = Column(String(50))
  route_text_color = Column(String(50))
  active = Column(String(50))
  # active = Column(Boolean, nullable=False, default=True)
