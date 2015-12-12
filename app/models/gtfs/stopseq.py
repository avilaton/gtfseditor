#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types, ForeignKey

from .gtfsbase import GTFSBase
from ..base import Base
from ..mixins import ToJSONMixin, Versioned


class StopSeq(Base, ToJSONMixin, Versioned, GTFSBase):
    __tablename__ = 'stop_seq'

    trip_id = Column(types.Integer,
                     ForeignKey("trips.trip_id", onupdate="CASCADE",
                                ondelete="CASCADE"),
                     primary_key=True)
    stop_id = Column(types.Integer,
                     ForeignKey("stops.stop_id", onupdate="CASCADE",
                                ondelete="CASCADE"),
                     primary_key=True)
    stop_sequence = Column(types.Integer, primary_key=True)
    stop_time = Column(types.String(50))
    shape_dist_traveled = Column(types.Float(precision=53))
