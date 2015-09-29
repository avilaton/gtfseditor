#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class CalendarDate(db.Model, Entity):
  __tablename__ = 'calendar_dates'
  service_id = db.Column(db.Integer, db.ForeignKey("calendar.service_id",
    onupdate="CASCADE"), primary_key=True)
  date = db.Column(db.String(50), primary_key=True)
  exception_type = db.Column(db.String(50), primary_key=True)
