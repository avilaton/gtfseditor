#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class Transfer(db.Model, Entity):
  __tablename__ = 'transfers'
  from_stop_id = db.Column(db.Integer, primary_key=True)
  to_stop_id = db.Column(db.Integer)
  transfer_type = db.Column(db.String(50))
