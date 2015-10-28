#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types, ForeignKey

from ..base import Base
from ..mixins import ToJSONMixin


class TripStartTime(Base, ToJSONMixin):

    __tablename__ = 'trips_start_times'
    __versioned__ = {
        'base_classes': (Base, ToJSONMixin, )
    }

    trip_id = Column(types.Integer,
                     ForeignKey("trips.trip_id", onupdate="CASCADE"),
                     primary_key=True)
    service_id = Column(types.Integer,
                        ForeignKey("calendar.service_id", onupdate="CASCADE"),
                        primary_key=True)
    start_time = Column(types.String(50), primary_key=True)
