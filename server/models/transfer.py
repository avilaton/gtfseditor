#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from base import Base, Entity

class Transfer(Base, Entity):
  __tablename__ = 'transfers'
  from_stop_id = Column(String(50), primary_key=True)
  to_stop_id = Column(String(50))
  transfer_type = Column(String(50))
