#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types

from ..base import Base
from ..mixins import ToJSONMixin


class FareRule(Base, ToJSONMixin):

    __tablename__ = 'fare_rules'
    __versioned__ = {
        'base_classes': (Base, ToJSONMixin, )
    }

    fare_id = Column(types.Integer, primary_key=True)
    route_id = Column(types.Integer)
    origin_id = Column(types.String(50))
    destination_id = Column(types.String(50))
    contains_id = Column(types.String(50))
