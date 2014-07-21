#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from base import Base, Entity

class Agency(Base, Entity):
  __tablename__ = 'agency'
  agency_id = Column(String(50), primary_key=True)
  agency_name = Column(String(50))
  agency_url = Column(String(50))
  agency_timezone = Column(String(50))
  agency_lang = Column(String(50))
  agency_phone = Column(String(50))

  def __repr__(self):
    return "<Agency: (id: '%s')>" % (self.agency_id)
