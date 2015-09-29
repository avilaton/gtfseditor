#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .entity import Entity


class FeedInfo(db.Model, Entity):
  __tablename__ = 'feed_info'
  feed_publisher_name = db.Column(db.String(50), primary_key=True)
  feed_publisher_url = db.Column(db.String(50))
  feed_lang = db.Column(db.String(50))
  feed_version = db.Column(db.String(50))
  feed_start_date = db.Column(db.String(50))
  feed_end_date = db.Column(db.String(50))
