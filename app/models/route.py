#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import Base
from .entity import Entity
from sqlalchemy import orm, Column, types, ForeignKey


class Route(Base, Entity):
  __tablename__ = 'routes'
  route_id = Column(types.Integer, primary_key=True)
  agency_id = Column(types.Integer, ForeignKey("agency.agency_id"))
  route_short_name = Column(types.String(50))
  route_long_name = Column(types.String(150))
  route_desc = Column(types.String(150))
  route_type = Column(types.String(50))
  route_color = Column(types.String(50))
  build_type = Column(types.String(50))
  route_text_color = Column(types.String(50))
  active = Column(types.Boolean, default=False)

