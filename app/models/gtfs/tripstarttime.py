#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import Base
from ..mixins import ToJSONMixin
from sqlalchemy import orm, Column, types, ForeignKey


class TripStartTime(Base, ToJSONMixin):

    __tablename__ = 'trips_start_times'

    trip_id = Column(types.Integer,
                     ForeignKey("trips.trip_id", onupdate="CASCADE"),
                     primary_key=True)
    service_id = Column(types.Integer,
                        ForeignKey("calendar.service_id", onupdate="CASCADE"),
                        primary_key=True)
    start_time = Column(types.String(50), primary_key=True)
