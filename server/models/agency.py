#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from server import Base

class Agency(Base):
  __tablename__ = 'agency'
  agency_id = Column(String(50), primary_key=True)
  agency_name = Column(String(50))
  agency_url = Column(String(50))
  agency_timezone = Column(String(50))
  agency_lang = Column(String(50))
  agency_phone = Column(String(50))

  def __repr__(self):
    return "<Agency: (id: '%s')>" % (self.agency_id)

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
