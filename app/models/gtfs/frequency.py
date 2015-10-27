#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import Base
from ..mixins import ToJSONMixin
from sqlalchemy import orm, Column, types, ForeignKey


class Frequency(Base, ToJSONMixin):

    __tablename__ = 'frequencies'

    trip_id = Column(types.Integer, ForeignKey("trips.trip_id", onupdate="CASCADE"),
                     primary_key=True)
    start_time = Column(types.String(50))
    end_time = Column(types.String(50))
    headway_secs = Column(types.Integer)
    exact_times = Column(types.String(50))
