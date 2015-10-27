#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import Base
from ..mixins import ToJSONMixin
from sqlalchemy import orm, Column, types, ForeignKey


class Trip(Base, ToJSONMixin):

    __tablename__ = 'trips'

    trip_id = Column(types.Integer, primary_key=True)
    route_id = Column(types.Integer, ForeignKey("routes.route_id"))
    service_id = Column(types.Integer)
    trip_headsign = Column(types.String(150))
    trip_short_name = Column(types.String(150))
    direction_id = Column(types.String(50))
    shape_id = Column(types.Integer)
    card_code = Column(types.String(50))
    active = Column(types.Boolean, default=False)
