#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class FareRule(db.Model, Entity):
  __tablename__ = 'fare_rules'
  fare_id = db.Column(db.Integer, primary_key=True)
  route_id = db.Column(db.Integer)
  origin_id = db.Column(db.String(50))
  destination_id = db.Column(db.String(50))
  contains_id = db.Column(db.String(50))
