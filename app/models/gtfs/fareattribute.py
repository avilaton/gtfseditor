#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types

from ..base import Base
from ..mixins import ToJSONMixin


class FareAttribute(Base, ToJSONMixin):

    __tablename__ = 'fare_attributes'
    __versioned__ = {}

    fare_id = Column(types.Integer, primary_key=True)
    price = Column(types.String(50))
    currency_type = Column(types.String(50))
    payment_method = Column(types.String(50))
    transfers = Column(types.String(50))
    transfer_duration = Column(types.String(50))
