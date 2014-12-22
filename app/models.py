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


class FeedInfo(db.Model, Entity):
  __tablename__ = 'feed_info'
  feed_publisher_name = db.Column(db.String(50), primary_key=True)
  feed_publisher_url = db.Column(db.String(50))
  feed_lang = db.Column(db.String(50))
  feed_version = db.Column(db.String(50))
  feed_start_date = db.Column(db.String(50))
  feed_end_date = db.Column(db.String(50))

class Agency(db.Model, Entity):
  __tablename__ = 'agency'
  agency_id = db.Column(db.String(50), primary_key=True)
  agency_name = db.Column(db.String(50))
  agency_url = db.Column(db.String(50))
  agency_timezone = db.Column(db.String(50))
  agency_lang = db.Column(db.String(50))
  agency_phone = db.Column(db.String(50))

class Calendar(db.Model, Entity):
  __tablename__ = 'calendar'
  service_id = db.Column(db.String(50), primary_key=True)
  start_date = db.Column(db.String(50))
  end_date = db.Column(db.String(50))
  monday = db.Column(db.String(50))
  tuesday = db.Column(db.String(50))
  wednesday = db.Column(db.String(50))
  thursday = db.Column(db.String(50))
  friday = db.Column(db.String(50))
  saturday = db.Column(db.String(50))
  sunday = db.Column(db.String(50))
