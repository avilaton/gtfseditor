#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types, ForeignKey

from .gtfsbase import GTFSBase
from ..base import Base
from ..mixins import ToJSONMixin, Versioned


class Frequency(Base, ToJSONMixin, Versioned, GTFSBase):
    __tablename__ = 'frequencies'

    trip_id = Column(types.Integer, ForeignKey("trips.trip_id", onupdate="CASCADE"),
                     primary_key=True)
    start_time = Column(types.String(50))
    end_time = Column(types.String(50))
    headway_secs = Column(types.Integer)
    exact_times = Column(types.String(50))
