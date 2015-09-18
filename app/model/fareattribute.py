#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class FareAttribute(db.Model, Entity):
  __tablename__ = 'fare_attributes'
  fare_id = db.Column(db.Integer, primary_key=True)
  price = db.Column(db.String(50))
  currency_type = db.Column(db.String(50))
  payment_method = db.Column(db.String(50))
  transfers = db.Column(db.String(50))
  transfer_duration = db.Column(db.String(50))
