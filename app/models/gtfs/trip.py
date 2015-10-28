#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types, ForeignKey

from ..base import Base
from ..mixins import ToJSONMixin


class Trip(Base, ToJSONMixin):

    __tablename__ = 'trips'
    __versioned__ = {
        'base_classes': (Base, ToJSONMixin, )
    }

    trip_id = Column(types.Integer, primary_key=True)
    route_id = Column(types.Integer, ForeignKey("routes.route_id"))
    service_id = Column(types.Integer)
    trip_headsign = Column(types.String(150))
    trip_short_name = Column(types.String(150))
    direction_id = Column(types.String(50))
    shape_id = Column(types.Integer)
    card_code = Column(types.String(50))
    active = Column(types.Boolean, default=False)
