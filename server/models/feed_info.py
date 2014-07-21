#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from base import Base, Entity

class FeedInfo(Base, Entity):
  __tablename__ = 'feed_info'
  feed_publisher_name = Column(String(50), primary_key=True)
  feed_publisher_url = Column(String(50))
  feed_lang = Column(String(50))
