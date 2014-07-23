#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, Sequence, String, Float
from base import Base, Entity

class Stop(Base, Entity):
  __tablename__ = 'stops'
  # stop_id = Column(Integer, Sequence('id_seq'), primary_key=True)
  stop_id = Column(String(50), primary_key=True)
  stop_code = Column(String(50))
  stop_desc = Column(String(50))
  stop_name = Column(String(50))
  stop_lat = Column(Float(precision=53))
  stop_lon = Column(Float(precision=53))
  stop_calle = Column(String(50))
  stop_numero = Column(String(50))
  stop_entre = Column(String(50))
  stop_esquina = Column(String(50))
