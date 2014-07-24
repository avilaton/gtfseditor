#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from base import Base, Entity

class CalendarDate(Base, Entity):
  __tablename__ = 'calendar_dates'
  service_id = Column(String(50), primary_key=True)
  date = Column(String(50), primary_key=True)
  exception_type = Column(String(50), primary_key=True)
