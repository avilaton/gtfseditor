#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class Agency(db.Model, Entity):
  __tablename__ = 'agency'
  agency_id = db.Column(db.Integer, primary_key=True)
  agency_name = db.Column(db.String(50))
  agency_url = db.Column(db.String(50))
  agency_timezone = db.Column(db.String(50))
  agency_lang = db.Column(db.String(50))
  agency_phone = db.Column(db.String(50))
