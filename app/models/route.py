#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class Route(db.Model, Entity):
  __tablename__ = 'routes'
  route_id = db.Column(db.Integer, primary_key=True)
  agency_id = db.Column(db.Integer, db.ForeignKey("agency.agency_id",
                                                  onupdate="CASCADE",
                                                  ondelete="SET NULL"))
  route_short_name = db.Column(db.String(50))
  route_long_name = db.Column(db.String(150))
  route_desc = db.Column(db.String(150))
  route_type = db.Column(db.String(50))
  route_color = db.Column(db.String(50))
  build_type = db.Column(db.String(50))
  route_text_color = db.Column(db.String(50))
  active = db.Column(db.Boolean, default=False)

