#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from base import Base, Entity

class FareAttribute(Base, Entity):
  __tablename__ = 'fare_attributes'
  fare_id = Column(String(50), primary_key=True)
  price = Column(String(50))
  currency_type = Column(String(50))
  payment_method = Column(String(50))
  transfers = Column(String(50))
  transfer_duration = Column(String(50))
