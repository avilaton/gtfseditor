#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class Stop(db.Model, Entity):
  __tablename__ = 'stops'
  stop_id = db.Column(db.Integer, primary_key=True)
  stop_code = db.Column(db.String(50))
  stop_desc = db.Column(db.String(250))
  stop_name = db.Column(db.String(250))
  stop_lat = db.Column(db.Float(precision=53))
  stop_lon = db.Column(db.Float(precision=53))
  stop_calle = db.Column(db.String(250))
  stop_numero = db.Column(db.String(50))
  stop_entre = db.Column(db.String(250))
  stop_esquina = db.Column(db.String(250))
