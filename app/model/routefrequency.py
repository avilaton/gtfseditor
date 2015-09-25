#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class RouteFrequency(db.Model, Entity):
  __tablename__ = 'route_frequencies'
  route_id = db.Column(db.Integer, db.ForeignKey("routes.route_id", onupdate="CASCADE"), primary_key=True)
  service_id = db.Column(db.Integer, db.ForeignKey("calendar.service_id",
    onupdate="CASCADE"), primary_key=True)
  start_time = db.Column(db.String(50), primary_key=True)
  end_time = db.Column(db.String(50), primary_key=True)
  headway_secs = db.Column(db.Integer)
