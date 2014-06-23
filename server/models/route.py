#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from server import Base

class Route(Base):
  __tablename__ = 'routes'
  route_id = Column(String(50), primary_key=True)
  agency_id = Column(String(50))
  route_short_name = Column(String(50))
  route_long_name = Column(String(50))
  route_desc = Column(String(50))
  route_type = Column(String(50))
  route_color = Column(String(50))
  route_text_color = Column(String(50))
  active = Column(String(50))
  # active = Column(Boolean, nullable=False, default=True)

  def __repr__(self):
    return "<Route: '%s' (route_short_name:'%s')>" % (self.route_id, 
      self.route_short_name)

  @property
  def as_dict(self):
    d = {}
    for column in self.__table__.columns:
      attr = getattr(self, column.name)
      if attr:
        d[column.name] = unicode(attr)
      else:
        d[column.name] = ''
    return d
