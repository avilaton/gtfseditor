#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from base import Base, Entity

class FareRule(Base, Entity):
  __tablename__ = 'fare_rules'
  fare_id = Column(String(50), primary_key=True)
  route_id = Column(String(50))
  origin_id = Column(String(50))
  destination_id = Column(String(50))
  contains_id = Column(String(50))
