#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class Calendar(db.Model, Entity):
  __tablename__ = 'calendar'
  service_id = db.Column(db.Integer, primary_key=True)
  service_name = db.Column(db.String(50))
  start_date = db.Column(db.String(50))
  end_date = db.Column(db.String(50))
  monday = db.Column(db.String(50))
  tuesday = db.Column(db.String(50))
  wednesday = db.Column(db.String(50))
  thursday = db.Column(db.String(50))
  friday = db.Column(db.String(50))
  saturday = db.Column(db.String(50))
  sunday = db.Column(db.String(50))
