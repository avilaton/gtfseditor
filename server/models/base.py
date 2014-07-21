#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, Sequence, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Entity(object):
  @property
  def as_dict(self):
    d = {}
    for column in self.__table__.columns:
      attr = getattr(self, column.name)
      if attr is not None:
        if isinstance(column.type, Float):
          d[column.name] = float(attr)
        else:
          d[column.name] = unicode(attr)
      else:
        d[column.name] = None
    return d
