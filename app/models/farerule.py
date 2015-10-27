#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import Base
from .entity import Entity
from sqlalchemy import orm, Column, types, ForeignKey


class FareRule(Base, Entity):

    __tablename__ = 'fare_rules'

    fare_id = Column(types.Integer, primary_key=True)
    route_id = Column(types.Integer)
    origin_id = Column(types.String(50))
    destination_id = Column(types.String(50))
    contains_id = Column(types.String(50))
