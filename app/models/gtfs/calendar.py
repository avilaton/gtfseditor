#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types

from .gtfsbase import GTFSBase
from ..base import Base
from ..mixins import ToJSONMixin, Versioned


class Calendar(Base, ToJSONMixin, Versioned, GTFSBase):
    __tablename__ = 'calendar'

    service_id = Column(types.Integer, primary_key=True)
    service_name = Column(types.String(50))
    start_date = Column(types.String(50))
    end_date = Column(types.String(50))
    monday = Column(types.String(50))
    tuesday = Column(types.String(50))
    wednesday = Column(types.String(50))
    thursday = Column(types.String(50))
    friday = Column(types.String(50))
    saturday = Column(types.String(50))
    sunday = Column(types.String(50))
