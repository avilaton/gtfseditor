#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class StopTime(db.Model, Entity):
  __tablename__ = 'stop_times'
  trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id", onupdate="CASCADE"), primary_key=True)
  stop_id = db.Column(db.Integer, db.ForeignKey("stops.stop_id",
    onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
  stop_sequence = db.Column(db.Integer, primary_key=True)
  arrival_time = db.Column(db.String(50))
  departure_time = db.Column(db.String(50))
  shape_dist_traveled = db.Column(db.Float(precision=53))