#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db


class ToJSONMixin(object):

  @property
  def to_json(self):
    d = {}
    for column in self.__table__.columns:
      attr = getattr(self, column.name)
      if attr is not None:
        if isinstance(column.type, db.Float):
          d[column.name] = float(attr)
        elif isinstance(column.type, db.Boolean):
          d[column.name] = attr
        elif isinstance(column.type, db.Integer):
          d[column.name] = int(attr)
        else:
          d[column.name] = unicode(attr)
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
