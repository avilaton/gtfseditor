#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref
from base import Base, Entity

class Agency(Base, Entity):
  __tablename__ = 'agency'
  agency_id = Column(String(50), primary_key=True)
  agency_name = Column(String(50))
  agency_url = Column(String(50))
  agency_timezone = Column(String(50))
  agency_lang = Column(String(50))
  agency_phone = Column(String(50))
  routes = relationship("Route", backref="agency")
