#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types

from ..base import Base
from ..mixins import ToJSONMixin


class FeedInfo(Base, ToJSONMixin):

    __tablename__ = 'feed_info'
    __versioned__ = {}

    feed_publisher_name = Column(types.String(50), primary_key=True)
    feed_publisher_url = Column(types.String(50))
    feed_lang = Column(types.String(50))
    feed_version = Column(types.String(50))
    feed_start_date = Column(types.String(50))
    feed_end_date = Column(types.String(50))
