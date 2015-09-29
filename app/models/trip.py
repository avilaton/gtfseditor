#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class Trip(db.Model, Entity):
  __tablename__ = 'trips'
  trip_id = db.Column(db.Integer, primary_key=True)
  route_id = db.Column(db.Integer, db.ForeignKey("routes.route_id"))
  service_id = db.Column(db.Integer)
  trip_headsign = db.Column(db.String(150))
  trip_short_name = db.Column(db.String(150))
  direction_id = db.Column(db.String(50))
  shape_id = db.Column(db.Integer)
  card_code = db.Column(db.String(50))
  active = db.Column(db.Boolean, default=False)
