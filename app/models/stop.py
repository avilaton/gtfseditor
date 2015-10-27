#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import Base
from .entity import Entity
from sqlalchemy import Column, types


class Stop(Base, Entity):

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
