#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types, ForeignKey

from .gtfsbase import GTFSBase
from ..base import Base
from ..mixins import ToJSONMixin, Versioned


class RouteFrequency(Base, ToJSONMixin, Versioned, GTFSBase):
    __tablename__ = 'route_frequencies'

    route_id = Column(types.Integer,
                      ForeignKey("routes.route_id", onupdate="CASCADE"),
                      primary_key=True)
    service_id = Column(types.Integer,
                        ForeignKey("calendar.service_id", onupdate="CASCADE"),
                        primary_key=True)
    start_time = Column(types.String(50), primary_key=True)
    end_time = Column(types.String(50), primary_key=True)
    headway_secs = Column(types.Integer)
