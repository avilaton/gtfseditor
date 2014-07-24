#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from base import Base, Entity

class Calendar(Base, Entity):
  __tablename__ = 'calendar'
  service_id = Column(String(50), primary_key=True)
  start_date = Column(String(50))
  end_date = Column(String(50))
  monday = Column(String(50))
  tuesday = Column(String(50))
  wednesday = Column(String(50))
  thursday = Column(String(50))
  friday = Column(String(50))
  saturday = Column(String(50))
  sunday = Column(String(50))
