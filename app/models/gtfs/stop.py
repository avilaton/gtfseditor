#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types

from .gtfsbase import GTFSBase
from ..base import Base
from ..mixins import ToJSONMixin, Versioned


class Stop(Base, ToJSONMixin, Versioned, GTFSBase):
    __tablename__ = 'stops'

    stop_id = Column(types.Integer, primary_key=True)
    stop_code = Column(types.String(50))
    stop_desc = Column(types.String(250))
    stop_name = Column(types.String(250))
    stop_lat = Column(types.Float(precision=53))
    stop_lon = Column(types.Float(precision=53))
    stop_calle = Column(types.String(250))
    stop_numero = Column(types.String(50))
    stop_entre = Column(types.String(250))
    stop_esquina = Column(types.String(250))
