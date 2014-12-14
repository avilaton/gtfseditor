#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app, request, url_for
from . import db


class Entity(object):
  @property
  def to_json(self):
    d = {}
    for column in self.__table__.columns:
      attr = getattr(self, column.name)
      if attr is not None:
        if isinstance(column.type, db.Float):
          d[column.name] = float(attr)
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


class Route(db.Model, Entity):
  __tablename__ = 'routes'
  route_id = db.Column(db.String(50), primary_key=True)
  agency_id = db.Column(db.String(50))
  route_short_name = db.Column(db.String(50))
  route_long_name = db.Column(db.String(150))
  route_desc = db.Column(db.String(150))
  route_type = db.Column(db.String(50))
  route_color = db.Column(db.String(50))
  route_text_color = db.Column(db.String(50))
  active = db.Column(db.String(50))
