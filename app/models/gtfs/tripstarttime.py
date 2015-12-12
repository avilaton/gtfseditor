#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types, ForeignKey

from .gtfsbase import GTFSBase
from ..base import Base
from ..mixins import ToJSONMixin, Versioned


class TripStartTime(Base, ToJSONMixin, Versioned, GTFSBase):
    __tablename__ = 'trips_start_times'

    trip_id = Column(types.Integer,
                     ForeignKey("trips.trip_id",
                                onupdate="CASCADE",
                                ondelete="CASCADE"),
                     primary_key=True)
    service_id = Column(types.Integer,
                        ForeignKey("calendar.service_id",
                                    onupdate="CASCADE",
                                    ondelete="CASCADE"),
                        primary_key=True)
    start_time = Column(types.String(50), primary_key=True)
