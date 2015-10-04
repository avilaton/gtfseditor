#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class Frequency(db.Model, Entity):
  __tablename__ = 'frequencies'
  trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id", onupdate="CASCADE"), primary_key=True)
  start_time = db.Column(db.String(50))
  end_time = db.Column(db.String(50))
  headway_secs = db.Column(db.Integer)
  exact_times = db.Column(db.String(50))
