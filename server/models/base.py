#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Float
from sqlalchemy import Boolean
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
        elif isinstance(column.type, Boolean):
          d[column.name] = bool(attr)
        else:
          d[column.name] = unicode(attr)
      elif isinstance(column.type, Boolean):
        d[column.name] = bool(attr)
      else:
        d[column.name] = None

    return d

  def __repr__(self):
    info = ['<', self.__class__.__name__, ': ']
    for col in self.__table__.primary_key.columns:
      attr = getattr(self, col.name)
      info.extend([col.name, '=', unicode(attr), ' '])
    info.append('>')
    return ('').join(info)