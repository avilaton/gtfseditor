#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types

from .gtfsbase import GTFSBase
from ..base import Base
from ..mixins import ToJSONMixin, Versioned


class Agency(Base, ToJSONMixin, Versioned, GTFSBase):
    __tablename__ = 'agency'

    agency_id = Column(types.Integer, primary_key=True)
    agency_name = Column(types.String(50))
    agency_url = Column(types.String(50))
    agency_timezone = Column(types.String(50))
    agency_lang = Column(types.String(50))
    agency_phone = Column(types.String(50))

