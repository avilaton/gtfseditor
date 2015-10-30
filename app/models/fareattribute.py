#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import Base
from .entity import Entity
from sqlalchemy import orm, Column, types, ForeignKey


class FareAttribute(Base, Entity):

    __tablename__ = 'fare_attributes'

    fare_id = Column(types.Integer, primary_key=True)
    price = Column(types.String(50))
    currency_type = Column(types.String(50))
    payment_method = Column(types.String(50))
    transfers = Column(types.String(50))
    transfer_duration = Column(types.String(50))
