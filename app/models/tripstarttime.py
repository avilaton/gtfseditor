#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class TripStartTime(db.Model, Entity):
  __tablename__ = 'trips_start_times'
  trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id", onupdate="CASCADE"), primary_key=True)
  service_id = db.Column(db.Integer, db.ForeignKey("calendar.service_id",
    onupdate="CASCADE"), primary_key=True)
  start_time = db.Column(db.String(50), primary_key=True)
