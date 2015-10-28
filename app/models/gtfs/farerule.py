#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types

from .gtfsbase import GTFSBase
from ..base import Base
from ..mixins import ToJSONMixin, Versioned


class FareRule(Base, ToJSONMixin, Versioned, GTFSBase):
    __tablename__ = 'fare_rules'

    fare_id = Column(types.Integer, primary_key=True)
    route_id = Column(types.Integer)
    origin_id = Column(types.String(50))
    destination_id = Column(types.String(50))
    contains_id = Column(types.String(50))
